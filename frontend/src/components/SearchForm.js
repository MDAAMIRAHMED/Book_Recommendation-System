// src/components/SearchForm.js
import React from 'react';

const SearchForm = ({ bookTitle, setBookTitle, handleSubmit }) => {
  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="book_title">Enter a Book Title:</label>
      <input
        type="text"
        id="book_title"
        value={bookTitle}
        onChange={(e) => setBookTitle(e.target.value)}
        required
      />
      <button type="submit">Get Recommendations</button>
    </form>
  );
};

export default SearchForm;