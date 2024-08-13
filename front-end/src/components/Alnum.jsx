import React, { useState } from 'react';
import axios from 'axios';
import './css folder/Alnum.css';

const Alnum = () => {
  const [status, setStatus] = useState('Idle');

  const startRecording = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/start_recording');
      setStatus(response.data.status);
    } catch (error) {
      setStatus('Error starting recording');
      console.error('Error:', error);
    }
  };

  const stopRecording = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/stop_recording');
      setStatus(response.data.status);
    } catch (error) {
      setStatus('Error stopping recording');
      console.error('Error:', error);
    }
  };

  const convertToSpeech = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/convert_to_speech', null, { responseType: 'blob' });
      const url = URL.createObjectURL(response.data);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'output.mp3';
      a.click();
      URL.revokeObjectURL(url);
      setStatus('Conversion complete');
    } catch (error) {
      setStatus('Error converting to speech');
      console.error('Error:', error);
    }
  };

  return (
    <div className="home-container">
      <h1 className="main-title">Alnum</h1>
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
        <div className="big-box" onClick={convertToSpeech}>
          <div className="small-box">
            <i className="fas fa-volume-up"></i> {/* Font Awesome speaker icon */}
          </div>
          <h2>Convert to Speech</h2>
        </div>
      </div>
      <p>Status: {status}</p>
    </div>
  );
};

export default Alnum;
