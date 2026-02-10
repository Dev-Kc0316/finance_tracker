import React from 'react';
import { FaSun, FaMoon } from 'react-icons/fa';

export default function ThemeToggle({ dark, setDark }) {
    return (
    <button 
    className='toggle-theme' 
    onClick={() => setDark(!dark)} aria-label='Toggle Theme'>
        {dark ? <FaSun size={25} color='yellow' /> : <FaMoon size={25} />}
    </button>
    );
}