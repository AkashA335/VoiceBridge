import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Signup from './components/Signup';
import AboutUs from './components/AboutUs';
import ContactUs from './components/ContactUs';
// import Drop from './components/Drop';
import SpeechToSign from './components/SpeechToSign';
import SignToSpeech from './components/SignToSpeech'; // Import SignToSpeech
import Alnum from './components/Alnum';
import Action from './components/Action';
const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/aboutus" element={<AboutUs />} />
        <Route path="/contactus" element={<ContactUs />} />
        {/* <Route path="/drop" element={<Drop />} /> */}
        <Route path="/speech-to-sign" element={<SpeechToSign />} />
        <Route path="/sign-to-speech" element={<SignToSpeech />} />
        <Route path="/alnum" element={<Alnum />} />
        <Route path="/action" element={<Action />} />
      </Routes>
    </Router>
  );
};

export default App;