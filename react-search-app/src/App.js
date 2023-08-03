import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [recommendedBooks, setRecommendedBooks] = useState([]);

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchSubmit = () => {
    fetchRecommendations();
    // Scroll to the top when the user submits the search
    window.scrollTo(0, 0);
  };

  const fetchRecommendations = () => {
    fetch('http://127.0.0.1:5000/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ search_terms: searchQuery }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        setRecommendedBooks(data.recommended_books_isbns);
      })
      .catch((error) => {
        console.error('Error occurred while fetching recommendations:', error);
      });
  };

  return (
    <div className="App">
      <header className="search-header">
        <h1>Book Search and Recommendation</h1>
        <div className="search-container">
          <input
            type="text"
            value={searchQuery}
            onChange={handleSearchChange}
            placeholder="Enter search terms..."
          />
          <button onClick={handleSearchSubmit}>Search</button>
        </div>
      </header>

      <main className="content">
        {recommendedBooks.length > 0 ? (
          <div className="recommendations">
            <h2>Recommended Book ISBNs:</h2>
            <ul>
              {recommendedBooks.map((isbn, index) => (
                <li key={index}>{isbn}</li>
              ))}
            </ul>
          </div>
        ) : (
          <p>No recommendations yet. Enter search terms and click "Search" to get book ISBNs.</p>
        )}
      </main>
    </div>
  );
};

export default App;
