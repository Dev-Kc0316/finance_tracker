import React from 'react';

export default function Sidebar() {
    const logout = () => {
        localStorage.removeItem("token");
        window.location.href = "/";
    };

    return (
        <aside className="sidebar">
            <h2>Finance Tracker</h2>
            <nav>
                <ul>
                    <li><a href="#">Dashboard</a></li>
                    <li><a href="#">Add Expense</a></li>
                </ul>
            </nav>
            <button onClick={logout}>Log Out</button>
        </aside>
    );
}