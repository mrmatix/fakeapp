import requests
import webbrowser
from bs4 import BeautifulSoup
from googlesearch import search


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
        print(f"No articles found related to '{query}'.")


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
        print(f"No articles found related to '{query}'.")


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


def search_nytimes(query):
    # Format the query for the NY Times search URL
    query = query.replace(' ', '+')

    # Send a GET request to the NY Times search URL
    url = f'https://www.nytimes.com/search?query={query}'
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the article links in the search results
    article_links = soup.select('div.css-e1lvw9 > a')

    # Print the number of articles found
    num_articles = len(article_links)
    if num_articles:
        print(f"Found {num_articles} articles related to '{query}':")
        print("Opening the first article in a new tab and the search results in another...")

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
            article_url = "https://www.nytimes.com/" + article_links[0]['href']
            print(f"\nArticle {i+1}:")
            print(f"Title: {article_title}")
            print(f"Description: {article_description}")
            print(f"URL: {article_url}")

            # Open the first article in a new tab
            if i == 0:
                print(f"\nOpening URL: {article_url}")
                webbrowser.open_new_tab(article_url)
    else:
        print(f"No articles found related to '{query}'.")
