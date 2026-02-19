import React, { useState } from 'react';
import { api } from '../services/api';

export default function ExpenseForm({ reload }) {
    const [title, setTitle] = useState("");
    const [amount, setAmount] = useState("");
    const [category, setCategory] = useState("");
    const [type, setType] = useState("expense");

    const addTransaction = async () => {
        try {
            await api.post("finance/add/", {type, title, amount: parseFloat(amount), category});
            setTitle(""); 
            setAmount(""); 
            setCategory("");

            reload();
        } catch (err) {
            console.error(err.response?.data || err.message);
        }
    };

    return(
        <div className="expense-form">
            <select value={type} onChange={(e) => setType(e.target.value)}>
                <option value="expense">Expense</option>
                <option value="income">Income</option>
            </select>

            <input type="text" placeholder='Title' value={title} onChange={(e) => setTitle(e.target.value)} />
            <input type="text" placeholder='Amount' value={amount} onChange={(e) => setAmount(e.target.value)} />
            <input type="text" placeholder='Category' value={category} onChange={(e) => setCategory(e.target.value)} />
            <button onClick={addTransaction}>Add Transaction</button>
        </div>
    );
}