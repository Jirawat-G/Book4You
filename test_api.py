import requests

# Define the base URL of the API
base_url = 'http://127.0.0.1:5000/'

# Define the endpoint to access the book recommendations
endpoint = 'recommend'

# User search terms
user_search_terms = "Android A.I. Applications"

# JSON data to send in the request
data = {
    'search_terms': user_search_terms
}

# Send the POST request to the API
response = requests.post(base_url + endpoint, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Get the recommended book titles from the response
    recommended_books = response.json()['recommended_books_isbns']
    
    # Print the recommended book titles
    print("Recommended Book ISBN:")
    for title in recommended_books:
        print(title)
else:
    print("Error: Unable to get book recommendations.")
