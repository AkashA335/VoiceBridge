import React from 'react';
import { useNavigate } from 'react-router-dom';
import './css folder/SignToSpeech.css';

const SignToSpeech = () => {
  const navigate = useNavigate();

  const handleAlnumClick = () => {
    navigate('/alnum');
  };

  const handleActionClick = () => {
    navigate('/action');
  };

  return (
    <div className="sign-to-speech-container">
      <h1>Sign to Speech Conversion</h1>
      <p>This page will handle the conversion of sign language to speech.</p>
      <div className="button-container">
        <button className="alnum-button" onClick={handleAlnumClick}>Alnum</button>
        <button className="action-button" onClick={handleActionClick}>Action</button>
      </div>
    </div>
  );
};

export default SignToSpeech;