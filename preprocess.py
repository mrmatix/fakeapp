import re


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
