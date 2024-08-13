import React, { useState } from 'react';
import axios from 'axios';
import './css folder/Action.css';

const Action = () => {
  const [status, setStatus] = useState('Idle');

  const startRecording = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/start');
      setStatus(response.data.message);
    } catch (error) {
      setStatus('Error starting recording');
      console.error('Error:', error);
    }
  };

  const stopRecording = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/stop');
      setStatus(response.data.message);
    } catch (error) {
      setStatus('Error stopping recording');
      console.error('Error:', error);
    }
  };

  const convertToAudio = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/predict', { responseType: 'json' });
      const { prediction, mp3_file } = response.data;
      setStatus(`Prediction: ${prediction}\nAudio file saved as ${mp3_file}`);
      // You might want to download the audio file as well
      // const audioUrl = URL.createObjectURL(new Blob([response.data], { type: 'audio/mp3' }));
      // const a = document.createElement('a');
      // a.href = audioUrl;
      // a.download = mp3_file;
      // a.click();
      // URL.revokeObjectURL(audioUrl);
    } catch (error) {
      setStatus('Error converting text to audio');
      console.error('Error:', error);
    }
  };

  return (
    <div className="home-container">
      <h1 className="main-title">Action</h1>
      <div className="boxes-wrapper">
        <div className="big-box" onClick={startRecording}>
          <div className="small-box">
            <i className="fas fa-video"></i> {/* Font Awesome video icon */}
          </div>
          <h2>Start Recording</h2>
        </div>
        <div className="big-box" onClick={stopRecording}>
          <div className="small-box">
            <i className="fas fa-stop"></i> {/* Font Awesome stop icon */}
          </div>
          <h2>Stop Recording</h2>
        </div>
        <div className="big-box" onClick={convertToAudio}>
          <div className="small-box">
            <i className="fas fa-volume-up"></i> {/* Font Awesome speaker icon */}
          </div>
          <h2>Convert to Audio</h2>
        </div>
      </div>
      <p>Status: {status}</p>
    </div>
  );
};

export default Action;
