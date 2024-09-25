// src/App.js
import React, { useState, useEffect } from 'react';
import SearchForm from './components/SearchForm';
import BookList from './components/BookList';
import { getRecommendations, getTopRecommendations } from './services/api';
import './styles/App.css';

const App = () => {
  const [bookTitle, setBookTitle] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [topRecommendations, setTopRecommendations] = useState([]);

  useEffect(() => {
    fetchTopRecommendations();
  }, []);

  const fetchTopRecommendations = async () => {
    try {
      const data = await getTopRecommendations();
      setTopRecommendations(data);
    } catch (error) {
      console.error('Error fetching top recommendations:', error);
      // Handle error (e.g., show error message to user)
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await getRecommendations(bookTitle);
      setRecommendations(data);
    } catch (error) {
      // Handle error (e.g., show error message to user)
    }
  };

  return (
    <div className="container">
      <h1>Book Recommendation System</h1>
      <SearchForm bookTitle={bookTitle} setBookTitle={setBookTitle} handleSubmit={handleSubmit} />
      {recommendations.length > 0 && (
        <BookList title="Recommendations" books={recommendations} />
      )}
      <BookList title="Top Recommendations" books={topRecommendations} />
    </div>
  );
};

export default App;