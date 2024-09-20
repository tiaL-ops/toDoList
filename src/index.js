import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';  // Import your styles
import App from './App';  // Import the main App component

// Render the App component into the 'root' div inside index.html
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
