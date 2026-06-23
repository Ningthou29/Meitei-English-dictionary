import React, { useState } from 'react';
import { mockHistory } from '../data/mockData';
import './History.css';

function History() {
  const [history, setHistory] = useState(mockHistory);

  const clearHistory = () => {
    if (window.confirm('Clear all history?')) {
      setHistory([]);
    }
  };

  const deleteEntry = (id) => {
    setHistory(history.filter(entry => entry.id !== id));
  };

  return (
    <div className="history-container">
      <div className="history-header">
        <h2>📜 Translation History</h2>
        {history.length > 0 && (
          <button className="clear-btn" onClick={clearHistory}>
            Clear All
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <div className="empty-state">
          <p> No translations yet.</p>
          <p style={{ fontSize: '14px', color: '#9CA3AF' }}>Start exploring the dictionary!</p>
        </div>
      ) : (
        <div className="history-list">
          {history.map((entry) => (
            <div key={entry.id} className="history-item">
              <div className="history-content">
                <div className="history-source">
                  <span className="label">From:</span>
                  <span className="text">{entry.source_text}</span>
                  <span className="lang">({entry.source_language})</span>
                </div>
                <div className="history-arrow">→</div>
                <div className="history-target">
                  <span className="label">To:</span>
                  <span className="text meitei">{entry.translated_text}</span>
                  <span className="lang">({entry.target_language})</span>
                </div>
              </div>
              <div className="history-actions">
                <button 
                  className="delete-btn"
                  onClick={() => deleteEntry(entry.id)}
                >
                  Delete
                </button>
              </div>
              <div className="history-time">
                {new Date(entry.created_at).toLocaleString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default History;