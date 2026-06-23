import React, { useState, useEffect } from 'react';
import { getHistory, deleteHistoryEntry, clearHistory } from '../services/api';
import './History.css';

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getHistory();
      setHistory(data.history);
    } catch (err) {
      setError('Failed to load history. Is the backend running?');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    if (window.confirm('Clear all history?')) {
      try {
        await clearHistory();
        await loadHistory();
      } catch (err) {
        setError('Failed to clear history.');
        console.error(err);
      }
    }
  };

  const handleDeleteEntry = async (id) => {
    try {
      await deleteHistoryEntry(id);
      await loadHistory();
    } catch (err) {
      setError('Failed to delete entry.');
      console.error(err);
    }
  };

  if (loading) {
    return <div className="loading">Loading history...</div>;
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <h2>📜 Translation History</h2>
        {history.length > 0 && (
          <button className="clear-btn" onClick={handleClearHistory}>
            🗑️ Clear All
          </button>
        )}
      </div>

      {error && (
        <div className="error-message">
          ⚠️ {error}
          <button onClick={loadHistory}>🔄 Retry</button>
        </div>
      )}

      {history.length === 0 ? (
        <div className="empty-state">
          <p>📝 No translations yet.</p>
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
                  onClick={() => handleDeleteEntry(entry.id)}
                >
                  🗑️ Delete
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