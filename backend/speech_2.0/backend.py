from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import threading
import queue
import time
import whisper
from PIL import Image, ImageSequence
import imageio

app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins; adjust as needed

# Configuration
fs = 44100  # Sample rate
channels = 2  # Number of channels
volume_factor = 2.0  # Volume increase factor
output_filename = 'recordedAudio.wav'
blocksize = 2048  # Increased block size
signs_folder = 'signs'
output_video_path = 'output.mp4'
fps = 10

# Queue for audio blocks
audio_queue = queue.Queue()
recording = threading.Event()
stop_event = threading.Event()

# Audio callback function
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

# Write audio blocks to file
def audio_writer():
    all_data = []
    try:
        while not stop_event.is_set():
            try:
                block = audio_queue.get(timeout=1)
                if block is None:
                    break
                block *= volume_factor
                block = np.clip(block, -1.0, 1.0)
                all_data.append(block)
            except queue.Empty:
                continue
    finally:
        if all_data:
            all_data = np.concatenate(all_data, axis=0)
            write(output_filename, fs, (all_data * np.iinfo(np.int16).max).astype(np.int16))

# Start recording
@app.route('/start_recording', methods=['POST'])
def start_recording():
    if recording.is_set():
        return jsonify({"status": "already recording"})
    recording.set()
    stop_event.clear()

    def recording_thread():
        stream = sd.InputStream(samplerate=fs, channels=channels, callback=audio_callback, blocksize=blocksize, latency='high')
        with stream:
            writer_thread = threading.Thread(target=audio_writer)
            writer_thread.start()
            while not stop_event.is_set():
                time.sleep(1)
            audio_queue.put(None)
            writer_thread.join()

    threading.Thread(target=recording_thread).start()
    return jsonify({"status": "recording started"})

# Stop recording
@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    if not recording.is_set():
        return jsonify({"status": "not recording"})
    recording.clear()
    stop_event.set()
    return jsonify({"status": "recording stopped"})

# Load GIF from local folder
def load_gif_from_local(gif_path):
    local_path = os.path.join(signs_folder, gif_path)
    if os.path.exists(local_path):
        try:
            gif = Image.open(local_path)
            gif.filename = gif_path
            return gif
        except Exception as e:
            print(f"Error loading GIF: {e}")
            return None
    else:
        print(f"Local GIF file does not exist at path: {local_path}")
        return None

# Fetch GIFs based on text
def fetch_gifs(text):
    gifs = []
    gif_path = f'{text}.gif'
    if os.path.exists(os.path.join(signs_folder, gif_path)):
        gifs.append(gif_path)
    return gifs

# Convert text to sign GIFs
def text_to_sign_gifs(text):
    gifs = []
    words = text.split()
    for word in words:
        gif_path = f"{word}.gif"
        if os.path.exists(os.path.join(signs_folder, gif_path)) and gif_path not in gifs:
            gif = load_gif_from_local(gif_path)
            if gif:
                gifs.append(gif)
    return gifs

# Create MP4 video from GIFs
def create_mp4_video(gifs):
    frames = []
    max_width = 0
    max_height = 0

    for gif in gifs:
        for frame in ImageSequence.Iterator(gif):
            frame_np = np.array(frame.convert("RGB"))
            frames.append(frame_np)
            max_width = max(max_width, frame_np.shape[1])
            max_height = max(max_height, frame_np.shape[0])

    resized_frames = []
    for frame_np in frames:
        resized_frame = np.zeros((max_height, max_width, 3), dtype=np.uint8)
        resized_frame[:frame_np.shape[0], :frame_np.shape[1], :] = frame_np
        resized_frames.append(resized_frame)

    if resized_frames:
        with imageio.get_writer(output_video_path, fps=fps) as writer:
            for frame_np in resized_frames:
                writer.append_data(frame_np)
        print(f"MP4 video saved as {output_video_path}")
    else:
        print("No frames to create MP4 video.")

# Perform conversion
@app.route('/perform_conversion', methods=['POST'])
def perform_conversion():
    try:
        model = whisper.load_model("small")
        result = model.transcribe(output_filename)
        text = result['text']
        gifs = text_to_sign_gifs(text)
        if gifs:
            create_mp4_video(gifs)
            return jsonify({"status": "success", "message": "Video created", "video_url": f"http://127.0.0.1:5000/get_video"})
        else:
            return jsonify({"status": "error", "message": "No GIFs found for the text"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Serve video file
@app.route('/get_video', methods=['GET'])
def get_video():
    return send_from_directory('.', output_video_path)

if __name__ == '__main__':
    app.run(debug=True)
