import React from 'react';
import ReactDOM from 'react-dom/client';  // Use react-dom/client for createRoot
import App from './App';

// Create a root container and render the App
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
