import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { api } from '../services/api';
import '../styles/login.css';

export default function Login(){
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const login = async (e) => {
        e.preventDefault();

        if(loading) return;

        setLoading(true);
        setError("");

        try{
            const res = await api.post("users/login/", {email, password});
            localStorage.setItem("token", res.data.access);
            localStorage.setItem("refresh", res.data.refresh);
            localStorage.setItem("user", JSON.stringify(res.data.user));
            
            navigate("/dashboard");
        } catch (err) {
            const msg = err.response?.data?.error || "Invalid email or password";

            setError(msg);
        } finally{
            setLoading(false);
        }
    };

    return(
        <div className="auth-container">
            <div className="login">
                <div className="login-page-image">
                    <h2>Personal Finance Tracker</h2>
                </div>
            <form onSubmit={login} className="login-form">
                <h2>Welcome Back</h2>
                <p>Login into your account</p>
                <input type="email" placeholder='example@gmail.com' value={email} onChange={(e) => setEmail(e.target.value)} />
                <input type="password" placeholder='***********' value={password} onChange={(e) => setPassword(e.target.value)} />

                {error && <p className='error-message'>{error}</p>}

                <button type='submit' disabled={loading}>
                    {loading? "logging in..." : "Login"}
                    </button>
                <p>
                    <Link to="/signup">Sign UP</Link> |{" "} 
                    <Link to="/forgot-password">Forgot Password?</Link>
                </p>
            </form>
            </div>
        </div>
    );
}