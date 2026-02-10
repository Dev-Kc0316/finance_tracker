import { useState } from 'react';
import { api } from '../services/api';
import './auth.css';

export default function ForgotPassword(){
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setMessage("");

        try {
            const res = await api.post("users/forgot-password/",{ email });
            setMessage("Reset code sent to your email");
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
                
                <button disabled={loading}>{loading ? "Sending..." : "Send Reset Code"}</button>
            </form>
        </div>
    );
}