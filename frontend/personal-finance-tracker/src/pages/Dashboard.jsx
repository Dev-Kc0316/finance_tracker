import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import ThemeToggle from '../components/ThemeToggle';
import ExpenseForm from '../components/ExpenseForm';
import Chart from '../components/Chart';
import { api } from '../services/api';
import '../styles/dashboard.css';


export default function Dashboard() {
    const [expenses, setExpenses] = useState([]);
    const [dark, setDark] = useState(false);
    const [username, setUsername] = useState("");
    const [balance, setBalance] = useState("");
    const [monthlyExpenses, setMonthlyExpenses] = useState(0);
    const [savingsRate, setSavingsRate] = useState(0);

 const loadDashboard = async () => {
   try {

      const { data } = await api.get("finance/dashboard/");

      setExpenses(data.transactions || []);
      setBalance(data.summary?.balance || 0);
      setUsername(data.user?.username ?? "");

   } catch(err){
      console.error(err.response?.data || err.message);
   }
};

useEffect(()=>{
   loadDashboard();
}, []);


    return(
        <div className={`dashboard ${dark ? "dark" : ""}`}>
            <Sidebar />
            <div className="main-content">
                <div className="dashboard-header">
                    <div className='hero-header'>
                    <h2>Welcome back, {username}</h2>
                    <p>Your financial overview today</p>
                    </div>
                    <div className="theme-toggle">
                    <ThemeToggle dark={dark} setDark={setDark} />
                    </div>
                </div>
                <div className="stats-row">
                    <div className="stat-card">
                        <h4>Total Balance</h4>
                        <h2>${balance.toLocaleString()}</h2>
                    </div>
                    <div className="stat-card">
                        <h4>Monthly Expenses</h4>
                        <h2>${monthlyExpenses.toLocaleString()}</h2>
                    </div>
                    <div className="stat-card">
                        <h4>Savings Rate</h4>
                        <h2>{savingsRate}%</h2>
                    </div>
                </div>
                <div className="dashboard-grid">
                    <div className="card">
                        <ExpenseForm reload={loadDashboard}/>
                    </div>
                    <div className="card chart">
                      <Chart expenses={expenses} />
                    </div>
                    <div className="card table">
                        <h3>Recent Expenses</h3>

                        <table className="expense-table">
                            <thead>
                                <tr>
                                    <th>Title</th>
                                    <th>Amount</th>
                                    <th>Category</th>
                                </tr>
                            </thead>

                            <tbody>
                                {expenses.map(exp => (
                                    <tr key={exp._id}>
                                        <td>{exp.title}</td>
                                        <td>${exp.amount}</td>
                                        <td>{exp.category}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
               
            </div>
        </div>
    );
}
