import React, { useState } from 'react';
import './App.css';
import Chatbot from './Chatbot.jsx';
import './Chatbot.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import LoginPage from './login.jsx';


function App() {

  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <div className="app">
    {!isLoggedIn ? (
      <LoginPage onLogin={handleLogin} />
    ) : (
      <Chatbot resetChat={() => {}} onLogout={handleLogout} />
    )}
  </div>
  );
}

export default App;
