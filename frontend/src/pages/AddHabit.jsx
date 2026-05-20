import React, { useState } from 'react';
import axios from 'axios';
import './AddHabit.css';

const API_BASE_URL = 'http://localhost:8000/api';

const AddHabit = () => {
  const [name, setName] = useState('');
  const [category, setCategory] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE_URL}/habits`, { name, category });
      setMessage('Habit added successfully!');
      setName('');
      setCategory('');
    } catch (error) {
      setMessage('Failed to add habit.');
      console.error(error);
    }
  };

  return (
    <div className="add-habit-container">
      <h1 className="text-gradient">Add New Habit</h1>
      <div className="glass-panel form-panel">
        <form onSubmit={handleSubmit} className="habit-form">
          <div className="form-group">
            <label>Habit Name</label>
            <input 
              type="text" 
              className="glass-input" 
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g., Drink Water"
              required 
            />
          </div>
          <div className="form-group">
            <label>Category</label>
            <input 
              type="text" 
              className="glass-input" 
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              placeholder="e.g., Health"
            />
          </div>
          <button type="submit" className="glass-button w-100">Save Habit</button>
          {message && <p className="form-message">{message}</p>}
        </form>
      </div>
    </div>
  );
};

export default AddHabit;
