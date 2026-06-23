import React, { useState } from 'react';
import Dictionary from './components/Dictionary';
import History from './components/History';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dictionary');

  return (
    <div className="App">
      <header className="app-header">
        <h1>📖 Meitei Mayek Dictionary</h1>
        <p>English ↔ Meitei Mayek</p>
      </header>

      <nav className="nav-tabs">
        <button 
          className={activeTab === 'dictionary' ? 'active' : ''}
          onClick={() => setActiveTab('dictionary')}
        >
          📖 Dictionary
        </button>
        <button 
          className={activeTab === 'history' ? 'active' : ''}
          onClick={() => setActiveTab('history')}
        >
          📜 History
        </button>
      </nav>

      <main className="main-content">
        {activeTab === 'dictionary' && <Dictionary />}
        {activeTab === 'history' && <History />}
      </main>
    </div>
  );
}

export default App;