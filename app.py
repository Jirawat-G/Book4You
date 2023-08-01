import pandas as pd
from flask import Flask, request, jsonify
from sklearn.metrics.pairwise import linear_kernel
from pythainlp.corpus import thai_stopwords
from pythainlp.util import normalize
from nltk.corpus import stopwords
from pythainlp.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
import string
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Load pre-trained models and data
books_data = pd.read_excel('BookToken.xlsx')

def clean_text(text):
    text = normalize(text)
    text = text.lower()
    # Use a single regular expression for cleaning
    replacements = {
        r'\t': ' ',
        r'\n': ' ',
        r'\r': ' ',
        r'“|”|…|’': ' ',
        r'\xa0': ' ',
        r'บท|หน่วยการเรียนรู้|หน่วยที่|ภาคผนวก [ก-ค]|ตอน|ที่|ๆ|chapter|part': ' '
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    # Remove digits and punctuation
    text = re.sub(r'[' + string.digits + string.punctuation + ']', ' ', text)
    return text

def tokenize_and_remove_stopwords(text):
    thaistopwords = set(thai_stopwords())
    english_stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    tokens = word_tokenize(text, keep_whitespace=False, engine='deepcut')

    tokens = [token for token in tokens if token not in english_stop_words and token not in thaistopwords]

    tokens = [stemmer.stem(token) for token in tokens]

    return tokens

def get_book_recommendations(user_search_terms):
    # Clean user search terms
    user_search_terms = clean_text(user_search_terms)

    # Tokenize cleaned user search terms
    user_search_terms = tokenize_and_remove_stopwords(user_search_terms)

    # Convert string representation of lists to actual Python lists in 'tokens_deepcut' column
    books_data['tokens_deepcut'] = books_data['tokens_deepcut'].apply(literal_eval)

    # Create the 'corpus' using cleaned user search terms and individual book tokens
    corpus = [' '.join(user_search_terms)] + [' '.join(tokens) for tokens in books_data['tokens_deepcut']]

    # Create a TF-IDF vectorizer and fit it on the corpus
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

    # Calculate cosine similarities between user search terms and book descriptions
    cosine_similarities = linear_kernel(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Get indices of books with highest similarity scores
    top_book_indices = cosine_similarities.argsort()[::-1]

    # Get recommended book ISBNs (limited to 5 in this example)
    recommended_books_isbns = [int(books_data.iloc[idx]['isbn']) for idx in top_book_indices[:5]]

    return recommended_books_isbns

@app.route('/recommend', methods=['POST'])
def recommend_books():
    data = request.json
    user_search_terms = data['search_terms']

    recommended_books_isbns = get_book_recommendations(user_search_terms)

    return jsonify({'recommended_books_isbns': recommended_books_isbns})

if __name__ == '__main__':
    app.run(debug=True)