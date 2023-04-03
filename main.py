import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import requests
from bs4 import BeautifulSoup
import webbrowser
from googlesearch import search

# Load the model
model = joblib.load('model/gnv.joblib')

# Load the TfidfVectorizer object used during training
vectorizer = joblib.load('vectorizer/tfidf.joblib')

webbrowser.BackgroundBrowser("C:/Program Files/Mozilla Firefox/firefox.exe")


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

# function for searching bbc


def search_reuters(query):
    # Format the query for the Reuters search URL
    query = query.replace(' ', '+')

    # Send a GET request to the Reuters search URL
    url = f'https://www.reuters.com/search/news?sortBy=date&dateRange=all&blob={query}'
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the article links in the search results
    article_links = soup.select('h3.search-result-title > a')

    # Print the number of articles found
    num_articles = len(article_links)
    if num_articles:
        print(f"Found {num_articles} articles related to '{query}':")
        print("Opening the first article in a new tab and the search results in another...")

        # Open the search results in the default browser
        webbrowser.open_new_tab(url)

        # Open the first article in a new tab
        article_url = "https://www.reuters.com" + article_links[0]['href']
        print(f"Opening URL: {article_url}")
        webbrowser.open_new_tab(article_url)
    else:
        print(f"No articles found related to '{query}'.")

# function for searching bbc


def search_bbc(query):
    # Format the query for the BBC search URL
    query = query.replace(' ', '+')

    # Send a GET request to the BBC search URL
    url = f'https://www.bbc.co.uk/search?q={query}&d=HOMEPAGE_GNL'
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Print response.content to see the HTML content DEBUG
    # print(soup)

    # Find all the article links in the search results
    article_links = soup.find_all(
        'a', {'class': 'ssrcss-rl2iw9-PromoLink e1f5wbog1'})

    # Print the number of articles found
    num_articles = len(article_links)
    if num_articles:
        print(f"Found {num_articles} articles related to '{query}':")
        print("Opening the first article in a new tab and the search results in another...")

        # Open the search results in the default browser
        webbrowser.open_new_tab(url)

        # Open the first article in a new tab
        article_url = article_links[0]['href']
        print(f"Opening URL: {article_url}")
        webbrowser.open_new_tab(article_url)
    else:
        print(f"No articles found related to '{query}'.")

# function for searching google


def search_google(query):
    # Perform a Google search for the query
    search_results = list(search(query, num_results=10))

    # Print the number of search results found
    num_results = len(search_results)
    if num_results:
        print(f"Found {num_results} search results related to '{query}':")
        print("Opening the first search result in a new tab and the search results in another...")

        # Open the search results in the default browser
        search_results_url = f'https://www.google.com/search?q={query}'
        webbrowser.open_new_tab(search_results_url)

        # Open the first search result in a new tab
        search_result_url = search_results[0]
        print(f"Opening URL: {search_result_url}")
        webbrowser.open_new_tab(search_result_url)
    else:
        print(f"No search results found related to '{query}'.")


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
    input_vector = vectorizer.transform([processed_input]).toarray()

    # Make predictions on the input vector
    preds = model.predict(input_vector)

    print("**********PRINTING THE DEBUGGING INFORMATION*****************")
    # Print the input_vector to check if the TfidfVectorizer is working correctly DEBUG
    print(f"input_vector = {input_vector}")

    # Print the preds to check the model prediction DEBUG
    print(f"preds = {preds}")

    # Print the preds[0] to check the model prediction DEBUG
    print(f"preds[0] = {preds[0]}")

    print("printing the probability of the prediction")
    # Print the probability of the prediction
    print(model.predict_proba(input_vector))

    print("printing the prediction")
    # Print the prediction
    print(model.predict(input_vector))
    print("**********PRINTING THE DEBUGGING INFORMATION*****************")

    # Print the prediction
    if preds[0] < 0.5:
        print("The phrase is possibly fake. This answer is based on the probability of the prediction.")
    else:
        print("The phrase is possibly real. This answer is based on the probability of the prediction.")

    # Ask the user if they want to search for the phrase in Reuters or BBC
    search_input = input(
        "Do you want to search for this phrase in Reuters / BBC? (R for Reuters/B for BBC/G for GOOGLE/Q for QUITTING THE PROGRAM): ")
    print(search_input)
    if search_input.lower() == 'r':
        search_reuters(user_input)
    elif search_input.lower() == 'b':
        search_bbc(user_input)
    elif search_input.lower() == 'g':
        search_google(user_input)
    elif search_input.lower() == 'q':
        break
    else:
        print("Invalid input.")
