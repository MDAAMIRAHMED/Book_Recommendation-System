// src/components/BookItem.js
import React from 'react';

const BookItem = ({ book }) => {
  return (
    <li>
      <div className="book-info">
        <img src={book.image_url} alt="Book Cover" className="book-cover" />
        <div className="book-details">
          <h3>{book.title}</h3>
          <p>by {book.author} | {book.year}</p>
          <p>Publisher: {book.publisher}</p>
          <p>{book.totalRatingCount} ratings</p>
        </div>
      </div>
    </li>
  );
};

export default BookItem;