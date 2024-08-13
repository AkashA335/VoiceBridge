import React, { useState } from 'react';
import axios from 'axios';

const SignToSpeech = () => {
  const [status, setStatus] = useState('Not Recording');
  const [transcribedText, setTranscribedText] = useState('');

  const startRecording = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/start_recording');
      if (response.data.status === 'recording started') {
        setStatus('Recording...');
      } else {
        alert('Recording is already in progress.');
      }
    } catch (error) {
      console.error('Error starting recording:', error);
      alert('Failed to start recording.');
    }
  };

  const stopRecording = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/stop_recording');
      if (response.data.status === 'recording stopped') {
        setStatus('Not Recording');
      } else {
        alert('Recording is not in progress.');
      }
    } catch (error) {
      console.error('Error stopping recording:', error);
      alert('Failed to stop recording.');
    }
  };

  const convertToSignLanguage = async () => {
    setStatus('Converting...');
    try {
      const response = await axios.post('http://127.0.0.1:5000/perform_conversion');
      if (response.data.status === 'conversion completed') {
        setStatus('Conversion Completed');
        setTranscribedText(response.data.transcribed_text);
        alert(`Transcribed Text: ${response.data.transcribed_text}`);
      } else {
        setStatus('Conversion Failed');
        alert(`Conversion failed: ${response.data.message}`);
      }
    } catch (error) {
      console.error('Error converting to sign language:', error);
      setStatus('Conversion Failed');
      alert('Failed to convert to sign language.');
    }
  };

  return (
    <div className="home-container">
      <h1 className="main-title">Sign Language Translator</h1>
      <p>Status: {status}</p>
      <div className="boxes-wrapper">
        <div className="big-box" onClick={startRecording}>
          <div className="small-box">🎤</div>
          <h2>Start Recording</h2>
        </div>
        <div className="big-box" onClick={stopRecording}>
          <div className="small-box">🛑</div>
          <h2>Stop Recording</h2>
        </div>
        <div className="big-box" onClick={convertToSignLanguage}>
          <div className="small-box">💬</div>
          <h2>Convert to Sign Language</h2>
        </div>
      </div>
      {transcribedText && (
        <div>
          <h2>Transcribed Text</h2>
          <p>{transcribedText}</p>
        </div>
      )}
    </div>
  );
};

export default SignToSpeech;
