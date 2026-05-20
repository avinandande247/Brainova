import React from 'react';
import './HabitCard.css';

const HabitCard = ({ habit, onLog }) => {
  return (
    <div className="habit-card glass-panel">
      <div className="habit-info">
        <h3 className="habit-name">{habit.name}</h3>
        <p className="habit-streak">Streak: {habit.streak || 0} days</p>
      </div>
      <button 
        className="glass-button habit-log-btn"
        onClick={() => onLog(habit.id || habit._id)}
      >
        Log
      </button>
    </div>
  );
};

export default HabitCard;
