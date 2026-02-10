import React, { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { Routes, Route, useLocation } from 'react-router-dom';
import Login from './pages/Login';
import Signup from './pages/Signup';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import Dashboard from './pages/Dashboard';
import './App.css';
import ProtectedRoute from './components/ProtectedRoute';
import PageTransition from './components/PageTransition';

export default function App() {
  const [dark, setDark] = useState(false);
  const location = useLocation();

  useEffect(() => {
    document.body.className = dark ? "dark" : "light";
  }, [dark]);

  return(
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={
          <PageTransition>
          <Login />
          </PageTransition>
          } />

        <Route path="/signup" element={
          <PageTransition>
          <Signup />
          </PageTransition>
          } />

        <Route path="/forgot-password" element={
          <PageTransition>
          <ForgotPassword />
          </PageTransition>
          } />

        <Route path="/reset-password" element={
          <PageTransition>
          <ResetPassword />
          </PageTransition>
          } />

        <Route path="/dashboard" element={
          <PageTransition>  
            <Dashboard  dark={dark} setDark={setDark}/>
          </PageTransition>
        } />
      </Routes>
    </AnimatePresence>
  );
}
