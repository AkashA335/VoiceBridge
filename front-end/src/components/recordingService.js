// recordingService.js
const API_BASE_URL = 'http://127.0.0.1:5000'; // Replace with your actual backend URL

export const startRecording = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/start_recording`, {
      method: 'POST',
    });
    const data = await response.json();
    if (data.status === 'recording started') {
      return true;
    } else {
      throw new Error('Recording already in progress');
    }
  } catch (error) {
    console.error('Error starting recording:', error);
    throw error;
  }
};

export const stopRecording = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/stop_recording`, {
      method: 'POST',
    });
    const data = await response.json();
    if (data.status === 'recording stopped') {
      return true;
    } else {
      throw new Error('Recording is not in progress');
    }
  } catch (error) {
    console.error('Error stopping recording:', error);
    throw error;
  }
};
