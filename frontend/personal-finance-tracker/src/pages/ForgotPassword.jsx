import { useEffect, useState } from 'react';
import { api } from '../services/api';
import './auth.css';

export default function ForgotPassword(){
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [cooldown, setCooldown] = useState(0);

    useEffect (() => {
                if(cooldown <= 0) return;

                const timer = setInterval(() => {
                    setCooldown(prev => prev -1);
                }, 1000);

                return () => clearInterval(timer);
            }, [cooldown]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setMessage("");

        if(cooldown > 0) return;

        try {
            const res = await api.post("users/forgot-password/",{ email });
            setMessage("Reset code sent to your email");

            setCooldown(60);
            

        } catch (err) {
            const msg = err.response?.data?.error || err.message || "Something went wrong";
            setError(msg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <form onSubmit={handleSubmit} className="auth-card">
                <h2>Forgot Password</h2>

                {error && <p className="error">{error}</p>}
                {message && <p className="success">{message}</p>}

                <input type="email" placeholder="Enter your email" value={email} required onChange={(e) => setEmail(e.target.value)} />
                
                <button type='submit' disabled={cooldown > 0}>
                    {cooldown > 0 ? `Resend in ${cooldown}s`: "Send Reset Email"}
                </button>
            </form>
        </div>
    );
}