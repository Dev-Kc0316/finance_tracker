import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import ExpenseForm from "../components/ExpenseForm";
import { api } from "../services/api";
import { FaBars } from "react-icons/fa";
import ThemeToggle from "../components/ThemeToggle";


export default function AddExpense({dark, setDark}) {

    const [expenses, setExpenses] = useState([]);
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [filters, setFilters] = useState({start: "", end: ""});

    const loadExpenses = async () => {
        try{
            const { data } = await api.get("finance/dashboard/", {
                params: {
                    ...(filters.start && { start: filters.start }),
                    ...(filters.end && { end: filters.end }),
                },
            });
            setExpenses(data.transactions || []);
        } catch(err) {
            console.error(err);
        }
    }

    useEffect(() => {
        loadExpenses();
    }, []);

    return (
        <div className={`dashboard ${dark? "dark" : ""}`}>
            <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />

            <div className="main-content">
                <div className="dashboard-header">
                    <div className="mobile-menu-btn" onClick={() => setSidebarOpen(true)}>
                    <FaBars />
                    </div>
                    <h2>Add Expense</h2>
                    <ThemeToggle dark={dark} setDark={setDark} />
                </div>

                <div className="card" style={{marginBottom: "0.625rem"}}>
                    <ExpenseForm reload={loadExpenses}/>
                </div>

                 <div className="card table">
                        <h3>Recent Expenses</h3>
                        
                        <div className="date-filter-bar">
                            <input 
                            type="date" 
                            value={filters.start}
                            onChange={(e) => 
                                setFilters({ ...filters, start: e.target.value })}
                            />

                            <input 
                            type="date" 
                            value={filters.end}
                            onChange={(e) => 
                                setFilters({ ...filters, end: e.target.value })
                            }
                            />

                            <button onClick={loadExpenses}>
                                Apply Filter
                            </button>

                        </div>

                        <div className="table-wrapper">
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
    )
}