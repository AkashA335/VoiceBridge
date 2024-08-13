import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './css folder/Drop.css';

const Drop = () => {
  const [fileType, setFileType] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const mode = localStorage.getItem('uploadMode');
    if (mode === 'speechToSign') {
      setFileType('audio/mpeg'); // Update to 'audio/mpeg'
    } else if (mode === 'signToSpeech') {
      setFileType('video/mp4');
    }
  }, []);

  const handleDrop = (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      console.log(`Dropped file type: ${file.type}`); // Debugging line
      if (file.type === fileType) {
        localStorage.setItem('uploadedFile', file.name);
        navigate('/speech-to-sign');
      } else {
        alert(`Please upload a file with ${fileType} format. You uploaded a ${file.type} file.`);
      }
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    console.log(`Selected file type: ${file.type}`); // Debugging line
    if (file && file.type === fileType) {
      localStorage.setItem('uploadedFile', file.name);
      navigate('/speech-to-sign');
    } else {
      alert(`Please upload a file with ${fileType} format. You uploaded a ${file.type} file.`);
    }
  };

  const handleClick = () => {
    document.getElementById('file-upload').click();
  };

  return (
    <div className="drop-wrapper">
      <div 
        className="drop-container" 
        onDrop={handleDrop} 
        onDragOver={handleDragOver}
        onClick={handleClick}
      >
        <h1>Drop or Upload Your File</h1>
        <p>Note: Only {fileType.split('/')[1]} format is accepted.</p>
        <input
          type="file"
          id="file-upload"
          accept={fileType}
          onChange={handleFileChange}
          style={{ display: 'none' }} // Hide the file input
        />
      </div>
    </div>
  );
};

export default Drop;
