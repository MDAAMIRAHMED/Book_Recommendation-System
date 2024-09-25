// src/services/api.js
import axios from 'axios';

const API_URL = 'http://localhost:5000';  // Adjust this to your Flask server's URL

export const getRecommendations = async (title) => {
  try {
    const response = await axios.get(`${API_URL}/recommend?title=${encodeURIComponent(title)}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    throw error;
  }
};

export const getTopRecommendations = async () => {
    try {
      const response = await axios.get(`${API_URL}/top_recommendations`);
      return response.data;
    } catch (error) {
      console.error('Error fetching top recommendations:', error);
      throw error;
    }
  };