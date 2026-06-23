import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

// ============ DICTIONARY ============

export const getAllWords = async (limit = 100, skip = 0) => {
  try {
    const response = await axios.get(`${API_URL}/dictionary?limit=${limit}&skip=${skip}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching words:', error);
    throw error;
  }
};

export const searchWord = async (word) => {
  try {
    const response = await axios.get(`${API_URL}/dictionary/search/${word}`);
    return response.data;
  } catch (error) {
    console.error('Error searching word:', error);
    throw error;
  }
};

export const addWord = async (english, roman_latin, meitei_mayek) => {
  try {
    const response = await axios.post(`${API_URL}/dictionary`, {
      english,
      roman_latin,
      meitei_mayek
    });
    return response.data;
  } catch (error) {
    console.error('Error adding word:', error);
    throw error;
  }
};

export const updateWord = async (id, english, roman_latin, meitei_mayek) => {
  try {
    const response = await axios.put(`${API_URL}/dictionary/${id}`, {
      english,
      roman_latin,
      meitei_mayek
    });
    return response.data;
  } catch (error) {
    console.error('Error updating word:', error);
    throw error;
  }
};

export const deleteWord = async (id) => {
  try {
    const response = await axios.delete(`${API_URL}/dictionary/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting word:', error);
    throw error;
  }
};

export const addMultipleWords = async (words) => {
  try {
    const response = await axios.post(`${API_URL}/dictionary/bulk`, words);
    return response.data;
  } catch (error) {
    console.error('Error adding multiple words:', error);
    throw error;
  }
};

// ============ HISTORY ============

export const addHistory = async (source_text, source_language, translated_text, target_language) => {
  try {
    const response = await axios.post(`${API_URL}/history`, null, {
      params: {
        source_text,
        source_language,
        translated_text,
        target_language
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error adding history:', error);
    throw error;
  }
};

export const getHistory = async (limit = 50) => {
  try {
    const response = await axios.get(`${API_URL}/history?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching history:', error);
    throw error;
  }
};

export const deleteHistoryEntry = async (id) => {
  try {
    const response = await axios.delete(`${API_URL}/history/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting history:', error);
    throw error;
  }
};

export const clearHistory = async () => {
  try {
    const response = await axios.delete(`${API_URL}/history`);
    return response.data;
  } catch (error) {
    console.error('Error clearing history:', error);
    throw error;
  }
};