import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './css folder/Home.css';
import logo from '../assets/logo.webp';
import Popup from './Popup'; // Ensure the correct path to Popup component
import Footer from './Footer'; // Import the Footer component

const Home = () => {
  const navigate = useNavigate();
  const [showPopup, setShowPopup] = useState(false);

  const handleBoxClickSpeechToSign = () => {
    localStorage.setItem('uploadMode', 'speechToSign');
    setShowPopup(true);
  };

  const handleBoxClickSignToSpeech = () => {
    localStorage.setItem('uploadMode', 'signToSpeech');
    setShowPopup(true);
  };

  const handleClosePopup = () => {
    setShowPopup(false);
    // navigate('/drop'); // Navigate to Drop page after closing the popup
  };

  return (
    <div className={`home-container ${showPopup ? 'blur' : ''}`}>
      <div className="page-title">
        <div className="logo-container">
          <img src={logo} alt="Logo" className="logo" />
        </div>
        <h1 className="main-title">Voice Bridge</h1>
      </div>
      <div className="boxes-wrapper">
        <div className="big-box" onClick={handleBoxClickSpeechToSign}>
          <h2>Speech To Sign</h2>
          <div className="small-box">🎤</div>
        </div>
        <div className="big-box" onClick={handleBoxClickSignToSpeech}>
          <h2>Sign To Speech</h2>
          <div className="small-box">👤</div>
        </div>
      </div>
      {showPopup && <Popup onClose={handleClosePopup} />}
      <Footer /> {/* Include the Footer component */}
    </div>
  );
};

export default Home;
