import tkinter as tk
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

# Define the GUI class


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        # Change size to 1024 x 768
        self.master.geometry("1024x768")

        # Change the background color to lightgrey
        self.master.configure(background="#F5F5F5")

        # make the same background color as the parent
        self.configure(background=self.master.cget("background"))

        # Change the title of the window
        self.master.title("Fake Reader")

        # Add a logo to the window
        logo = tk.PhotoImage(file="logo/logo.png")
        logo_label = tk.Label(self, image=logo)
        logo_label.image = logo
        logo_label.pack(pady=10)

        # Create a heading label
        self.heading_label = tk.Label(
            self, text="Welcome to the Fake Reader App where you can check if a phrase is real or fake.", font=("Helvetica", 16))
        self.heading_label.pack(pady=20)

        # Create a label for the query entry box
        self.query_label = tk.Label(
            self, text="Enter a query:", font=("Helvetica", 14))
        self.query_label.pack()

        # Create an entry box for the user to enter a query
        self.query_entry = tk.Entry(self, width=70, font=("Helvetica", 14))
        self.query_entry.pack(pady=10)

        # Create a prediction label
        self.prediction_label = tk.Label(
            self, text="Prediction:", font=("Helvetica", 14))
        self.prediction_label.pack(pady=10)

        # Create a prediction button
        self.predict_button = tk.Button(
            self, text="Predict", command=self.prediction, bg='#4169E1', fg='white', font=("Helvetica", 14), width=10)
        self.predict_button.pack(pady=10)

        # Create a button for searching the BBC
        self.search_bbc_button = tk.Button(
            self, text="Search BBC", command=self.search_bbc, bg='#4169E1', fg='white', font=("Helvetica", 14), width=15)
        self.search_bbc_button.pack(side="left", padx=5)

        # Create a button for searching Reuters
        self.search_reuters_button = tk.Button(
            self, text="Search Reuters", command=self.search_reuters, bg='#4169E1', fg='white', font=("Helvetica", 14), width=15)
        self.search_reuters_button.pack(side="left", padx=5)

        # Create a button for searching Google
        self.search_google_button = tk.Button(
            self, text="Search Google", command=self.search_google, bg='#4169E1', fg='white', font=("Helvetica", 14), width=15)
        self.search_google_button.pack(side="left", padx=5)

        # Create a button for searching NY Times
        self.search_nytimes_button = tk.Button(
            self, text="Search NY Times", command=self.search_nytimes, bg='#4169E1', fg='white', font=("Helvetica", 14), width=15)
        self.search_nytimes_button.pack(side="left", padx=5)

        # Create a button for showing the about message
        self.about_button = tk.Button(
            self, text="About", command=self.show_about, bg='#4169E1', fg='white', font=("Helvetica", 14), width=10)
        self.about_button.pack(side="right", padx=5)

        # Create a fixed-width empty label to separate the About and Quit buttons
        self.empty_label = tk.Label(self, width=10)
        self.empty_label.pack(side="right")

        # Create a button for quitting the application
        self.quit_button = tk.Button(
            self, text="Quit", command=self.master.destroy, bg='red', fg='white', font=("Helvetica", 14), width=10)
        self.quit_button.pack(side="right", padx=5)

    def show_about(self):
        # Create a new window
        about_window = tk.Toplevel(self)

        # Set the title of the window
        about_window.title("About")

        # Set the size of the window
        about_window.geometry("600x400")

        # Add a label to the window with some text
        about_label = tk.Label(
            about_window, text="This is a fake news detector app. It uses a machine learning model to predict whether a phrase is real or fake. Simply enter a phrase, preferably a political one, and click the Predict button. The app will then predict whether the phrase is real or fake. You can also search for the phrase on the BBC, Reuters, Google and NY Times websites.", wraplength=500)
        about_label.pack(pady=20)

        # Add a button to close the window
        close_button = tk.Button(about_window, text="Close",
                                 command=about_window.destroy)
        close_button.pack(pady=10)

    # Define the functions for each search button

    def search_bbc(self):
        query = self.query_entry.get()
        # Format the query for the BBC search URL
        query_text = query.replace(' ', '+')

        # Send a GET request to the BBC search URL
        url = f'https://www.bbc.co.uk/search?q={query_text}&d=HOMEPAGE_GNL'
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
            print(f"Found {num_articles} articles related to '{query_text}':")
            print(
                "Opening the first article in a new tab and the search results in another...")

            # Open the search results in the default browser
            webbrowser.open_new_tab(url)

            # Print information for each article found
            for i, link in enumerate(article_links):
                article_title = link.text
                article_description = link.find_next('p')
                if article_description:
                    article_description = article_description.text
                else:
                    article_description = "No description available."
                article_url = link['href']
                print(f"\nArticle {i+1}:")
                print(f"Title: {article_title}")
                print(f"Description: {article_description}")
                print(f"URL: {article_url}")

                # Open the first article in a new tab
                if i == 0:
                    print(f"\nOpening URL: {article_url}")
                    webbrowser.open_new_tab(article_url)
        else:
            print(f"No articles found related to '{query_text}'.")

    def search_reuters(self):
        query = self.query_entry.get()
        # Format the query for the Reuters search URL
        query_text = query.replace(' ', '+')

        # Send a GET request to the Reuters search URL
        url = f'https://www.reuters.com/search/news?sortBy=date&dateRange=all&blob={query_text}'
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the article links in the search results
        article_links = soup.select('h3.search-result-title > a')

        # Print the number of articles found
        num_articles = len(article_links)
        if num_articles:
            print(f"Found {num_articles} articles related to '{query_text}':")
            print(
                "Opening the first article in a new tab and the search results in another...")

            # Open the search results in the default browser
            webbrowser.open_new_tab(url)

            # Print information for each article found
            for i, link in enumerate(article_links):
                article_title = link.text
                article_description = link.find_previous('p')
                if article_description:
                    article_description = article_description.text
                else:
                    article_description = "No description available."
                article_url = "https://www.reuters.com" + link['href']
                print(f"\nArticle {i+1}:")
                print(f"Title: {article_title}")
                print(f"Description: {article_description}")
                print(f"URL: {article_url}")

                # Open the first article in a new tab
                if i == 0:
                    print(f"\nOpening URL: {article_url}")
                    webbrowser.open_new_tab(article_url)
        else:
            print(f"No articles found related to '{query_text}'.")

    def search_google(self):
        query = self.query_entry.get()
        # Perform a Google search for the query
        search_results = list(search(query, num_results=10))

        # Print the number of search results found
        num_results = len(search_results)
        if num_results:
            print(f"Found {num_results} search results related to '{query}':")
            print(
                "Opening the first search result in a new tab and the search results in another...")

            # Open the search results in the default browser
            search_results_url = f'https://www.google.com/search?q={query}'
            webbrowser.open_new_tab(search_results_url)

            # Open the first search result in a new tab
            search_result_url = search_results[0]
            print(f"Opening URL: {search_result_url}")
            webbrowser.open_new_tab(search_result_url)
        else:
            print(f"No search results found related to '{query}'.")

    def search_nytimes(self):
        query = self.query_entry.get()
        # Format the query for the NY Times search URL
        query_text = query.replace(' ', '+')

        # Send a GET request to the NY Times search URL
        url = f'https://www.nytimes.com/search?query={query_text}'
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the article links in the search results
        article_links = soup.select('div.css-e1lvw9 > a')

        # Print the number of articles found
        num_articles = len(article_links)
        if num_articles:
            print(f"Found {num_articles} articles related to '{query_text}':")
            print(
                "Opening the first article in a new tab and the search results in another...")

            # Open the search results in the default browser
            webbrowser.open_new_tab(url)

            # Print information for each article found
            for i, link in enumerate(article_links):
                article_title = link.find('h4', {'class': 'css-2fgx4k'}).text
                article_description = link.find('p', {'class': 'css-16nhkrn'})
                if article_description:
                    article_description = article_description.text
                else:
                    article_description = "No description available."
                article_url = "https://www.nytimes.com/" + \
                    article_links[0]['href']
                print(f"\nArticle {i+1}:")
                print(f"Title: {article_title}")
                print(f"Description: {article_description}")
                print(f"URL: {article_url}")

                # Open the first article in a new tab
                if i == 0:
                    print(f"\nOpening URL: {article_url}")
                    webbrowser.open_new_tab(article_url)
        else:
            print(f"No articles found related to '{query_text}'.")

    def prediction(self):
        # Get user input
        user_input = self.query_entry.get()
        # Preprocess the user input
        processed_input = preprocess_text(user_input)

        # Convert the preprocessed input to a numerical representation using TfidfVectorizer
        input_vector = vectorizer.transform([processed_input]).toarray()

        # Make predictions on the input vector
        preds = model.predict(input_vector)

        # Show prediction
        if preds[0] < 0.5:
            prediction_str = "The phrase is possibly fake. This answer is based on the probability of the prediction."
        else:
            prediction_str = "The phrase is possibly real. This answer is based on the probability of the prediction."
        self.prediction_label.config(text=prediction_str)


# Create the GUI
root = tk.Tk()
app = Application(master=root)
app.mainloop()
