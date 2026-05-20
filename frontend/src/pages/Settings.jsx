import React from 'react';

const Settings = () => {
  return (
    <div className="settings-container">
      <h1 className="text-gradient">Settings</h1>
      
      <div className="glass-panel p-2 mt-2">
        <h3>Theme Preferences</h3>
        <p>Current theme: <strong>Dark Mode (Glassmorphism)</strong></p>
        
        <h3 className="mt-2">Notifications</h3>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <input type="checkbox" id="push-notif" defaultChecked />
          <label htmlFor="push-notif">Enable Push Notifications</label>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginTop: '0.5rem' }}>
          <input type="checkbox" id="email-notif" />
          <label htmlFor="email-notif">Enable Email Summaries</label>
        </div>

        <h3 className="mt-2">Account</h3>
        <button className="glass-button" style={{ marginTop: '1rem' }}>Log Out</button>
      </div>
    </div>
  );
};

export default Settings;
