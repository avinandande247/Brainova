import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="sidebar glass-panel">
      <div className="sidebar-header">
        <h2 className="primary-text">Brainova</h2>
      </div>
      <ul className="nav-links">
        <li>
          <NavLink to="/" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            Dashboard
          </NavLink>
        </li>
        <li>
          <NavLink to="/add-habit" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            Add Habit
          </NavLink>
        </li>
        <li>
          <NavLink to="/reminders" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            Projects & Reminders
          </NavLink>
        </li>
        <li>
          <NavLink to="/analytics" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            Analytics
          </NavLink>
        </li>
        <li>
          <NavLink to="/settings" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            Settings
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
