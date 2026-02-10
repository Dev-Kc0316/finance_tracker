import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { api } from '../services/api';
import '../styles/signup.css';

export default function Signup() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [balance, setBalance] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const formatNumber = (value) => {
        if (!value) return "";

        const numbersOnly = value.replace(/\D/g, "");

        return new Intl.NumberFormat("en-US").format(numbersOnly);
    }

    const signup = async () => {
        try{
            await api.post("users/signup/", {
                email,
                username,
                password,
                balance: balance.replace(/,/g, "")
            });
            setMessage("Signup successful! Login now");
            setError("");

            navigate("/");
        } catch (err){
            setError(err.response?.data?.error || "Signup failed")
            setMessage("");
    
        } 
    };

    return(
        <div className="auth-container">
            <div className="signup-form">
                <h2>Create Account</h2>
                <p>Start tracking your finances today</p>

                <input type="email" placeholder='example@gmail.com' value={email} onChange={(e) => setEmail(e.target.value)} />

                <input type="text" placeholder='Username' value={username} onChange={(e) => setUsername(e.target.value)} />

                <div className="currency-wrapper">
                    <span className="currency-symbol">$</span>

                <input type="text" inputMode='decimal' placeholder='Starting Balance' value={balance} onChange={(e) => {
                    const formatted = formatNumber(e.target.value);
                    setBalance(formatted)
                } } />
                </div>

                <input type="password" placeholder='***********' value={password} onChange={(e) => setPassword(e.target.value)} />
                
                {message && <p className="success-msg">{message}</p>}{error && <p className="error-msg">{error}</p>}

                <button onClick={signup}>Sign Up</button>
                <p>Already have an account? | <Link to="/">Login</Link></p>
            </div>
        </div>
    );
}