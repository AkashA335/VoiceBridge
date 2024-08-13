import tkinter as tk
from tkinter import messagebox
import requests

class SignLanguageTranslatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sign Language Translator")
        
        self.status_label = tk.Label(master, text="Status: Not Recording")
        self.status_label.pack()

        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack()

        self.convert_button = tk.Button(master, text="Convert to Sign Language", command=self.convert_to_sign_language)
        self.convert_button.pack()

    def start_recording(self):
        response = requests.post('http://127.0.0.1:5000/start_recording')
        if response.json().get("status") == "recording started":
            self.status_label.config(text="Status: Recording...")
        else:
            messagebox.showerror("Error", "Recording is already in progress.")

    def stop_recording(self):
        response = requests.post('http://127.0.0.1:5000/stop_recording')
        if response.json().get("status") == "recording stopped":
            self.status_label.config(text="Status: Not Recording")
        else:
            messagebox.showerror("Error", "Recording is not in progress.")

    def convert_to_sign_language(self):
        self.status_label.config(text="Status: Converting...")
        response = requests.post('http://127.0.0.1:5000/perform_conversion')
        if response.json().get("status") == "conversion completed":
            self.status_label.config(text="Status: Conversion Completed")
            transcribed_text = response.json().get("transcribed_text")
            messagebox.showinfo("Transcription", f"Transcribed Text: {transcribed_text}")
        else:
            self.status_label.config(text="Status: Conversion Failed")
            messagebox.showerror("Error", f"Conversion failed: {response.json().get('error')}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageTranslatorApp(root)
    root.mainloop()
