import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import requests
from bs4 import BeautifulSoup

# Load the XGB model
model = joblib.load('model/xgb.joblib')

# Load the TfidfVectorizer object used during training
vectorizer = joblib.load('vectorizer/tfidf.joblib')


def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove non-alphabetic characters
    text = re.sub('[^a-zA-Z]', ' ', text)

    # Tokenize the text
    words = text.split()

    # Join the words back into a string with space as separator
    clean_text = ' '.join(words)

    return clean_text


def search_reuters(query):
    # Format the query for the Reuters search URL
    query = query.replace(' ', '+')

    # Send a GET request to the Reuters search URL
    url = f'https://www.reuters.com/search/news?sortBy=date&dateRange=all&blob={query}'
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the article links in the search results
    article_links = soup.find_all('a', {'class': 'search-result-title'})

    # Print the article links
    if article_links:
        print(f"Found {len(article_links)} articles related to '{query}':")
        for link in article_links:
            print(link['href'])
    else:
        print(f"No articles found related to '{query}'.")


def search_bbc(query):
    # Format the query for the Reuters search URL
    query = query.replace(' ', '+')

    # Send a GET request to the Reuters search URL
    url = f'https://www.bbc.co.uk/search?q={query}&d=HOMEPAGE_GNL'
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the article links in the search results
    article_links = soup.find_all('a', {'class': 'search-result-title'})

    # Print the article links
    if article_links:
        print(f"Found {len(article_links)} articles related to '{query}':")
        for link in article_links:
            print(link['href'])
    else:
        print(f"No articles found related to '{query}'.")


while True:
    print("Welcome to the Fake Reader App where you can check if a phrase is real or fake.")
    # Get user input
    user_input = input("Enter a phrase or 'quit' to exit: ")

    # Add this line at the beginning of the while loop DEBUG
    print(f"user_input = {user_input}")

    if user_input == 'quit':
        break

    # Preprocess the user input
    processed_input = preprocess_text(user_input)

    # Print the processed_input to check if the preprocessing is working correctly DEBUG
    print(f"processed_input = {processed_input}")

    # Convert the preprocessed input to a numerical representation using TfidfVectorizer
    input_vector = vectorizer.transform([processed_input])

    # Print the input_vector to check if the TfidfVectorizer is working correctly DEBUG
    print(f"input_vector = {input_vector}")

    # Make predictions on the input vector
    preds = model.predict(input_vector)

    # Print the preds to check the model prediction DEBUG
    print(f"preds = {preds}")

    # Print the prediction
    if preds[0] < 0.7:
        print("The phrase is possibly fake.")
    else:
        print("The phrase is possibly real.")

    # Ask the user if they want to search for the phrase in Reuters or BBC
    search_input = input(
        "Do you want to search for this phrase in Reuters / BBC? (R for Reuters/B for BBC): ")
    if search_input.lower() == 'R':
        search_reuters(user_input)
    elif search_input.lower() == 'B':
        search_bbc(user_input)
