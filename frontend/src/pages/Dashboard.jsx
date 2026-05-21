import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import MetricCard from '../components/MetricCard';
import HabitCard from '../components/HabitCard';
import './Dashboard.css';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000') + '/api';

const Dashboard = () => {
  const [progress, setProgress] = useState(null);
  const [insights, setInsights] = useState(null);
  const [habits, setHabits] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [progressRes, insightsRes, habitsRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/progress`),
          axios.get(`${API_BASE_URL}/insights`),
          axios.get(`${API_BASE_URL}/habits`)
        ]);
        
        setProgress(progressRes.data);
        setInsights(insightsRes.data);
        setHabits(habitsRes.data);
      } catch (error) {
        console.error("Error fetching data", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  const handleLogHabit = async (id) => {
    try {
      const today = new Date().toISOString().split('T')[0];
      await axios.post(`${API_BASE_URL}/habits/${id}/log`, { date: today, status: 'completed' });
      // Refresh habits after log
      const res = await axios.get(`${API_BASE_URL}/habits`);
      setHabits(res.data);
    } catch (error) {
      console.error("Error logging habit", error);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  const completionRate = progress?.completion_rate || 0;
  const pieData = [
    { name: 'Completed', value: completionRate },
    { name: 'Remaining', value: 100 - completionRate }
  ];
  const COLORS = ['#F63366', 'rgba(255,255,255,0.1)'];

  return (
    <div className="dashboard-container">
      <h1 className="text-gradient">Welcome Back</h1>
      
      <div className="grid-cards mb-2">
        <MetricCard 
          title="Daily Score" 
          value={`${completionRate}%`} 
          subtitle="Habits completed today" 
        />
        <MetricCard 
          title="Current Streak" 
          value={progress?.current_streak || 0} 
          subtitle="Days in a row" 
        />
        <MetricCard 
          title="Total Badges" 
          value={progress?.badges?.length || 0} 
          subtitle="Achievements unlocked" 
        />
      </div>

      <div className="dashboard-main-grid">
        <div className="glass-panel progress-section">
          <h3>Daily Progress</h3>
          <div className="progress-ring-container">
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={70}
                  outerRadius={90}
                  startAngle={90}
                  endAngle={-270}
                  dataKey="value"
                  stroke="none"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="progress-text">
              <h2>{completionRate}%</h2>
            </div>
          </div>
        </div>

        <div className="glass-panel habits-section">
          <h3>Today's Habits</h3>
          <div className="habits-list">
            {Array.isArray(habits) && habits.length > 0 ? (
              habits.map(habit => (
                <HabitCard key={habit.id || habit._id} habit={habit} onLog={handleLogHabit} />
              ))
            ) : (
              <p>No habits for today. Add one!</p>
            )}
          </div>
        </div>
      </div>

      {insights && (
        <div className="glass-panel mt-2 p-2">
          <h3>AI Insights</h3>
          <p>{insights.message || "Keep up the good work!"}</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
