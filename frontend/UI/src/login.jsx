import React, { useState } from 'react';
import './login.css';

const LoginPage = ({onLogin}) => {
    const [username, setUsername] = useState(''); 
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onLogin();
    };

    return (
        <div className="login-container">
          <form className="login-box" onSubmit={handleSubmit}>
            <h2>Hospital ChatDB Admin Login</h2>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Login</button>
          </form>
        </div>
      );
};

export default LoginPage;