import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const Analytics = () => {
  // Mock data for MVP
  const data = [
    { name: 'Mon', completed: 4 },
    { name: 'Tue', completed: 5 },
    { name: 'Wed', completed: 3 },
    { name: 'Thu', completed: 6 },
    { name: 'Fri', completed: 4 },
    { name: 'Sat', completed: 7 },
    { name: 'Sun', completed: 5 },
  ];

  return (
    <div className="analytics-container">
      <h1 className="text-gradient">Analytics</h1>
      
      <div className="glass-panel p-2 mt-2">
        <h3>Weekly Performance</h3>
        <div style={{ width: '100%', height: 300, marginTop: '2rem' }}>
          <ResponsiveContainer>
            <BarChart data={data}>
              <XAxis dataKey="name" stroke="#a0a0b0" />
              <YAxis stroke="#a0a0b0" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0E1117', border: '1px solid rgba(255,255,255,0.08)' }} 
                itemStyle={{ color: '#F63366' }} 
              />
              <Bar dataKey="completed" fill="#F63366" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
