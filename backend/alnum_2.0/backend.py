from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from threading import Thread, Lock
from ultralytics import YOLO
import time
import os
from gtts import gTTS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load the custom YOLOv8 model
model = YOLO("models/yolov8_custom.pt")

# Initialize variables to keep track of previous predictions and timestamps
previous_prediction = None
last_prediction_time = 0
is_recording = False
lock = Lock()
stability_duration = 2  # seconds

def record_predictions():
    global previous_prediction, last_prediction_time, is_recording
    
    with open("output.txt", "w") as output_file:
        while is_recording:
            results = model.predict(source=0, show=True, stream=True)

            for result in results:
                if not is_recording:
                    return

                current_prediction = [model.names[int(cls)] for cls in result.boxes.cls]
                current_time = time.time()

                with lock:
                    if current_prediction != previous_prediction:
                        previous_prediction = current_prediction
                        last_prediction_time = current_time
                    elif current_time - last_prediction_time >= stability_duration:
                        if current_prediction:
                            prediction_str = ", ".join(current_prediction)
                            output_file.write(prediction_str + "\n")
                            output_file.flush()
                            last_prediction_time = current_time  # Update timestamp after writing

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global is_recording
    if not is_recording:
        is_recording = True
        thread = Thread(target=record_predictions)
        thread.start()
        return jsonify({"status": "Recording started"}), 200
    return jsonify({"status": "Recording already in progress"}), 400

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global is_recording
    if is_recording:
        is_recording = False
        return jsonify({"status": "Recording stopped"}), 200
    return jsonify({"status": "No recording in progress"}), 400

@app.route('/convert_to_speech', methods=['POST'])
def convert_to_speech():
    try:
        with open("output.txt", "r") as file:
            text = file.read()

        if not text.strip():
            return jsonify({"status": "No text to convert"}), 400

        tts = gTTS(text=text, lang='en')
        audio_path = "output.mp3"
        tts.save(audio_path)
        
        return send_file(audio_path, as_attachment=True)
    except Exception as e:
        return jsonify({"status": f"Error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
