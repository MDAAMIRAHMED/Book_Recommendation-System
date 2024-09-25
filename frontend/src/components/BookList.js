// src/components/BookList.js
import React from 'react';
import BookItem from './BookItem';

const BookList = ({ title, books }) => {
  return (
    <div>
      <h2>{title}:</h2>
      <ul>
        {books.map((book, index) => (
          <BookItem key={index} book={book} />
        ))}
      </ul>
    </div>
  );
};

export default BookList;