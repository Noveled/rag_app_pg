import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import './App.css';
import Chat from './components/Chat';

const App = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="app-container">
      <header className={`header ${isSidebarOpen ? 'header-shrink' : ''}`}>
        <div className='flex gap-2'>
          { !isSidebarOpen && (
            <div>
              <button className="open-btn" onClick={toggleSidebar}>≡</button>
              <button className="open-btn" onClick={toggleSidebar}>≡</button>
            </div>
          )}
          <span>RAG DEMO</span>
        </div>
        <div className="logo">
          <h1>My Website</h1>
        </div>
        
      </header>

      <div className="content-container">
        <Sidebar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
        <main className={`main-content ${isSidebarOpen ? 'content-shrink' : ''}`}>
          <Chat />
        </main>
      </div>
    </div>
  );
};

export default App;
