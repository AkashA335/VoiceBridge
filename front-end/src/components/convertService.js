// convertService.js
const API_BASE_URL = 'http://127.0.0.1:5000'; // Replace with your actual backend URL

export const convertToSignLanguage = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/perform_conversion`, {
      method: 'POST',
    });
    const data = await response.json();
    if (data.status === 'conversion completed') {
      return {
        success: true,
        transcribedText: data.transcribed_text,
        videoPath: data.video_path,
      };
    } else {
      throw new Error(data.message || 'Conversion failed');
    }
  } catch (error) {
    console.error('Error converting to sign language:', error);
    throw error;
  }
};
