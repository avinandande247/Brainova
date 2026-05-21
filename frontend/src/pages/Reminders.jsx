import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Reminders.css';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000') + '/api';

const Reminders = () => {
  const [reminders, setReminders] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [remRes, projRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/reminders`),
          axios.get(`${API_BASE_URL}/projects`)
        ]);
        setReminders(remRes.data || []);
        setProjects(projRes.data || []);
      } catch (error) {
        console.error("Error fetching reminders or projects", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="reminders-container">
      <h1 className="text-gradient">Projects & Reminders</h1>
      
      <div className="reminders-grid mt-2">
        <div className="glass-panel p-2">
          <h3>Reminders</h3>
          {Array.isArray(reminders) && reminders.length > 0 ? (
            <ul className="reminders-list">
              {reminders.map((rem, i) => (
                <li key={i} className="reminder-item">
                  <span className="reminder-title">{rem.title || rem.message}</span>
                  <span className="reminder-time primary-text">{rem.time}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p>No upcoming reminders.</p>
          )}
        </div>

        <div className="glass-panel p-2">
          <h3>Active Projects</h3>
          {Array.isArray(projects) && projects.length > 0 ? (
            <div className="projects-list">
              {projects.map((proj, i) => (
                <div key={i} className="project-card">
                  <h4>{proj.name}</h4>
                  <p>{proj.description}</p>
                </div>
              ))}
            </div>
          ) : (
            <p>No active projects found.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Reminders;
