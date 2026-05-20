import React from 'react';
import './MetricCard.css';

const MetricCard = ({ title, value, subtitle, icon }) => {
  return (
    <div className="metric-card glass-panel">
      <div className="metric-header">
        <h4 className="metric-title">{title}</h4>
        {icon && <span className="metric-icon">{icon}</span>}
      </div>
      <div className="metric-content">
        <h2 className="metric-value primary-text">{value}</h2>
        {subtitle && <p className="metric-subtitle">{subtitle}</p>}
      </div>
    </div>
  );
};

export default MetricCard;
