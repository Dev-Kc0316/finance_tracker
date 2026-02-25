import { NavLink } from "react-router-dom";
import { FaTimes } from "react-icons/fa";
import { FaRegChartBar } from 'react-icons/fa';
import { FaReceipt } from "react-icons/fa";
import { FaSignOutAlt } from "react-icons/fa";

export default function Sidebar({ open, setOpen }) {
    const logout = () => {
        localStorage.removeItem("token");
        window.location.href = "/";
    };

    return(
        <>
        <div className={`sidebar-overlay ${open? "show" : ""}`} onClick={() => setOpen(false)} 
        />
        <aside className={`sidebar ${open? "open" : ""}`}>
            

            <div className="sidebar-header">
                <h2>Finance Tracker</h2>

                <div className="mobile-close-btn" onClick={() => setOpen(false)}>
                    <FaTimes size={16}/>
                </div>
            </div>

            <nav>
                <ul>
                    <li><NavLink to="/dashboard">Dashboard <FaRegChartBar size={17} /></NavLink></li>
                    <li><NavLink to="/add-expense" >Add Expense <FaReceipt size={17} /></NavLink></li>
                </ul>
            </nav>

            <button onClick={logout} > Log Out <FaSignOutAlt size={17} /></button>
        </aside>
        </>
    );
}