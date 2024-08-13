from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import threading
import os
from gtts import gTTS

app = Flask(__name__)

# Enable CORS
CORS(app)

# Load the pre-trained model
model = load_model('./models/action.h5')

# Initialize MediaPipe and other variables
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
sequence = []
sentence = []
threshold = 0.8
actions = np.array(['hello', 'peace'])
cap = None  # Initialize cap to None

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert color space from BGR to RGB
    image.flags.writeable = False                   # Mark image as not writeable
    results = model.process(image)                  # Process the image and get the results
    image.flags.writeable = True                    # Mark image as writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert color space back to BGR
    return image, results

def extract_keypoints(results):
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([lh, rh])

def start_detection():
    global cap
    global sequence
    global sentence
    global threshold

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        image, results = mediapipe_detection(frame, holistic)
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]

        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            prediction = actions[np.argmax(res)]
            confidence = np.max(res)

            if confidence > threshold:
                if len(sentence) == 0 or (sentence[-1] != prediction):
                    sentence.append(prediction)

            cv2.putText(image, ' '.join(sentence), (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Gesture Detection', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def save_text_to_mp3(text):
    tts = gTTS(text=text, lang='en')
    mp3_filename = "prediction.mp3"
    tts.save(mp3_filename)
    return mp3_filename

@app.route('/start', methods=['POST'])
def start():
    global cap
    global sequence
    global sentence
    global threshold

    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return jsonify(message="Failed to open camera"), 500
        threading.Thread(target=start_detection, daemon=True).start()
        return jsonify(message="Detection started")
    return jsonify(message="Detection is already running")

@app.route('/stop', methods=['POST'])
def stop():
    global cap
    if cap and cap.isOpened():
        cap.release()
        cv2.destroyAllWindows()
        return jsonify(message="Detection stopped")
    return jsonify(message="Detection is not running")

@app.route('/predict', methods=['GET'])
def predict():
    global sentence
    prediction = ' '.join(sentence)
    if prediction:
        with open('prediction.txt', 'w') as file:
            file.write(prediction)
        mp3_filename = save_text_to_mp3(prediction)
        return jsonify(prediction=prediction, mp3_file=mp3_filename)
    return jsonify(prediction="No prediction")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
