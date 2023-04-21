import webbrowser
from search import search_bbc, search_nytimes, search_reuters, search_google
from model import model, vectorizer
from preprocess import preprocess_text

# Open the Firefox browser
webbrowser.BackgroundBrowser("C:/Program Files/Mozilla Firefox/firefox.exe")
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

    # Ask the user if they want to search for the phrase in Reuters or BBC or Google or NYTimes or Quit
    search_input = input(
        "Do you want to search for this phrase in Reuters / BBC / Google / NYTimes / or Quit? \n(R for Reuters/B for BBC/G for GOOGLE/N for NYTimes/Q for QUITTING THE PROGRAM): ")
    print(search_input)
    if search_input.lower() == 'r':
        search_reuters(user_input)
    elif search_input.lower() == 'b':
        search_bbc(user_input)
    elif search_input.lower() == 'g':
        search_google(user_input)
    elif search_input.lower() == 'n':
        search_nytimes(user_input)
    elif search_input.lower() == 'q':
        break
    else:
        print("Invalid input.")
