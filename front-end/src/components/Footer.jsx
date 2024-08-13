import React from 'react';
import './css folder/Footer.css'; // Ensure the correct path to Footer.css

const Footer = () => {
  return (
    <footer className="footer-container">
      <div className="footer-content">
        <p>&copy; Grind@2024 📅</p>
        <div className="contact-info">
          <p>Email: <a href="mailto:a.akash030305@gmail.com">a.akash030305@gmail.com</a>, <a href="mailto:aarthielumalaimaha@gmail.com">aarthielumalaimaha@gmail.com</a> ✉️</p>
          <p>Phone: <a href="tel:+1234567890">+1234567890</a>, <a href="tel:+0987654321">+0987654321</a> 📞</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
