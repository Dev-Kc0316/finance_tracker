import { useState } from 'react';
import { api } from '../services/api';
import './auth.css';

export default function ResetPassword() {
    const [form, setform] = useState({
        email: "",
        code: "",
        password: ""
    });

    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const handleChange = (e) => {
        setform({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setMessage("");

        try {
            const res = await api.post("users/reset-password/", form);
            setMessage("Password reset successful.");
        } catch (err) {
            const msg = err.response?.data?.error || err.message;
            setError(msg);
        }
    };

    return (
        <div className="auth-container">
            <form onSubmit={handleSubmit} className="auth-card">
                <h2>Reset Password</h2>

                {error && <p className='error'>{error}</p>}
                {message && <p className='success'>{message}</p>}

                <input type="email" name='email' placeholder='Email' required onChange={handleChange} />

                <input type="text" name='code' placeholder='Reset Code' required onChange={handleChange} />

                <input type="password" name='password' placeholder='New Password' required onChange={handleChange} />

                <button>Reset Password</button>
            </form>
        </div>
    );
}