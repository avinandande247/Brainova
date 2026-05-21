import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import './Analytics.css';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000') + '/api';

const Analytics = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/analytics`);
        setData(res.data);
      } catch (error) {
        console.error("Error fetching analytics", error);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) return <div className="loading">Loading analytics...</div>;

  const dayData = data?.day_of_week?.map(d => ({
    name: d.Day?.substring(0, 3) || d.day?.substring(0, 3) || '',
    completed: d.Completions ?? d.completions ?? 0
  })) || [];

  const habitStats = data?.habit_stats || [];
  const missedHabits = data?.missed_habits || [];
  const totalCompletions = data?.total_completions || 0;
  const totalHabits = data?.total_habits || 0;

  // Calculate best streak from habit stats
  const bestStreak = habitStats.length > 0
    ? Math.max(...habitStats.map(h => h.streak || 0))
    : 0;

  // Calculate average completion rate
  const avgRate = habitStats.length > 0
    ? (habitStats.reduce((sum, h) => sum + (h.completion_rate || 0), 0) / habitStats.length).toFixed(1)
    : 0;

  return (
    <div className="analytics-container">
      <h1 className="text-gradient">Analytics</h1>

      {/* Summary Cards */}
      <div className="analytics-summary mt-2">
        <div className="glass-panel summary-card">
          <span className="summary-value">{totalHabits}</span>
          <span className="summary-label">Active Habits</span>
        </div>
        <div className="glass-panel summary-card">
          <span className="summary-value">{totalCompletions}</span>
          <span className="summary-label">Total Completions</span>
        </div>
        <div className="glass-panel summary-card">
          <span className="summary-value">{bestStreak}</span>
          <span className="summary-label">Best Streak</span>
        </div>
        <div className="glass-panel summary-card">
          <span className="summary-value">{avgRate}%</span>
          <span className="summary-label">Avg Completion</span>
        </div>
      </div>

      <div className="analytics-grid">
        {/* Weekly Performance Chart */}
        <div className="glass-panel chart-panel">
          <h3>Weekly Performance</h3>
          {Array.isArray(dayData) && dayData.length > 0 ? (
            <div style={{ width: '100%', height: 250 }}>
              <ResponsiveContainer>
                <BarChart data={dayData}>
                  <XAxis dataKey="name" stroke="#a0a0b0" fontSize={12} />
                  <YAxis stroke="#a0a0b0" fontSize={12} allowDecimals={false} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0E1117', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px' }}
                    itemStyle={{ color: '#F63366' }}
                  />
                  <Bar dataKey="completed" fill="#F63366" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p className="empty-state">No completion data yet. Start logging habits!</p>
          )}
        </div>

        {/* Most Missed Habits */}
        <div className="glass-panel chart-panel">
          <h3>⚠️ Most Missed (Last 30 Days)</h3>
          {Array.isArray(missedHabits) && missedHabits.length > 0 ? (
            <ul className="missed-list">
              {missedHabits.slice(0, 5).map((m, i) => (
                <li key={i} className="missed-item">
                  <span className="missed-name">{m.Habit || m.habit}</span>
                  <span className="missed-count">{m.Missed || m.missed} missed</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="empty-state">No missed habits — great job! 🎉</p>
          )}
        </div>

        {/* Per-Habit Breakdown */}
        <div className="glass-panel chart-panel full-width">
          <h3>Habit Breakdown</h3>
          {Array.isArray(habitStats) && habitStats.length > 0 ? (
            <ul className="habit-stats-list">
              {habitStats.map((h, i) => (
                <li key={i} className="habit-stat-item">
                  <div>
                    <span className="habit-stat-name">{h.name}</span>
                    {h.category && <span className="habit-stat-category">({h.category})</span>}
                  </div>
                  <div className="habit-stat-details">
                    <span className="stat-badge streak">🔥 {h.streak} day{h.streak !== 1 ? 's' : ''}</span>
                    <span className="stat-badge rate">{h.completion_rate}%</span>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="empty-state">Add some habits to see your breakdown here.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Analytics;
