import tkinter as tk
import requests
from tkinter import messagebox

# Define the base URL for the Flask server
BASE_URL = "http://127.0.0.1:5000"

def start_recording():
    response = requests.post(f"{BASE_URL}/start_recording")
    status = response.json().get("status", "Unknown error")
    status_label.config(text=status)

def stop_recording():
    response = requests.post(f"{BASE_URL}/stop_recording")
    status = response.json().get("status", "Unknown error")
    status_label.config(text=status)

def convert_to_speech():
    try:
        response = requests.post(f"{BASE_URL}/convert_to_speech")
        if response.status_code == 200:
            with open("output.mp3", "wb") as f:
                f.write(response.content)
            # Optionally, you can use a media player to play the audio file
            # For example, using the `os.system` call to play audio on different platforms
            import os
            os.system("start output.mp3")  # For Windows
            # os.system("open output.mp3")  # For macOS
            # os.system("xdg-open output.mp3")  # For Linux
        else:
            messagebox.showerror("Error", response.json().get("status", "Unknown error"))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the Tkinter UI
root = tk.Tk()
root.title("YOLOv8 Recording Interface")

# Start Button
start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

# Stop Button
stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.pack(pady=10)

# Convert to Speech Button
convert_button = tk.Button(root, text="Convert to Speech", command=convert_to_speech)
convert_button.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="Status: Idle")
status_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
