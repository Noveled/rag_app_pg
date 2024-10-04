import React from 'react';
import './Sidebar.css';

const Sidebar = ({ isOpen, toggleSidebar }) => {
  return (
    <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <button className="close-btn" onClick={toggleSidebar}>X</button>
      <div className="sidebar-content">
        <p>여기에 사이드바 내용</p>
      </div>
    </div>
  );
};

export default Sidebar;
