import React, { useState } from 'react';
import { mockDictionary } from '../data/mockData';
import './Dictionary.css';

function Dictionary() {
  const [searchTerm, setSearchTerm] = useState('');
  const [words, setWords] = useState(mockDictionary);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newWord, setNewWord] = useState({
    english: '',
    roman_latin: '',
    meitei_mayek: ''
  });

  const filteredWords = words.filter(word =>
    word.english.toLowerCase().includes(searchTerm.toLowerCase()) ||
    word.roman_latin.toLowerCase().includes(searchTerm.toLowerCase()) ||
    word.meitei_mayek.includes(searchTerm)
  );

  const handleAddWord = (e) => {
    e.preventDefault();
    if (newWord.english && newWord.roman_latin && newWord.meitei_mayek) {
      setWords([...words, { ...newWord }]);
      setNewWord({ english: '', roman_latin: '', meitei_mayek: '' });
      setShowAddForm(false);
    }
  };

  return (
    <div className="dictionary-container">
      <div className="dictionary-header">
        <h2>📖 Dictionary</h2>
        <button 
          className="add-word-btn"
          onClick={() => setShowAddForm(!showAddForm)}
        >
          {showAddForm ? '✕ Close' : '➕ Add Word'}
        </button>
      </div>

      <div className="search-bar">
        <input
          type="text"
          placeholder="🔍 Search words..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <span className="word-count">{filteredWords.length} words</span>
      </div>

      {showAddForm && (
        <form className="add-word-form" onSubmit={handleAddWord}>
          <input
            type="text"
            placeholder="English"
            value={newWord.english}
            onChange={(e) => setNewWord({...newWord, english: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Roman Latin"
            value={newWord.roman_latin}
            onChange={(e) => setNewWord({...newWord, roman_latin: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Meitei Mayek"
            value={newWord.meitei_mayek}
            onChange={(e) => setNewWord({...newWord, meitei_mayek: e.target.value})}
            required
          />
          <button type="submit">✅ Add Word</button>
        </form>
      )}

      <div className="word-grid">
        {filteredWords.map((word, index) => (
          <div key={index} className="word-card">
            <div className="word-english">{word.english}</div>
            <div className="word-roman">{word.roman_latin}</div>
            <div className="word-meitei">{word.meitei_mayek}</div>
          </div>
        ))}
      </div>

      {filteredWords.length === 0 && (
        <div className="empty-state">
          <p>No words found. Try a different search!</p>
        </div>
      )}
    </div>
  );
}

export default Dictionary;