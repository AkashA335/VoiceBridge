import tkinter as tk
from tkinter import messagebox
import requests

# Define the Flask server URL
FLASK_SERVER_URL = 'http://localhost:5000'

class GestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Translator")
        self.root.geometry("400x200")

        # Create buttons
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=10)

        self.convert_to_audio_button = tk.Button(root, text="Convert to Audio", command=self.convert_to_audio)
        self.convert_to_audio_button.pack(pady=10)

    def start_recording(self):
        response = requests.post(f"{FLASK_SERVER_URL}/start")
        if response.status_code == 200:
            messagebox.showinfo("Start Recording", response.json().get("message"))
        else:
            messagebox.showerror("Error", "Failed to start recording")

    def stop_recording(self):
        response = requests.post(f"{FLASK_SERVER_URL}/stop")
        if response.status_code == 200:
            messagebox.showinfo("Stop Recording", response.json().get("message"))
        else:
            messagebox.showerror("Error", "Failed to stop recording")

    def convert_to_audio(self):
        response = requests.get(f"{FLASK_SERVER_URL}/predict")
        if response.status_code == 200:
            result = response.json()
            prediction = result.get("prediction")
            mp3_file = result.get("mp3_file")
            messagebox.showinfo("Conversion Complete", f"Prediction: {prediction}\nAudio file saved as {mp3_file}")
        else:
            messagebox.showerror("Error", "Failed to convert text to audio")

# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = GestureApp(root)
    root.mainloop()
