import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the model
model = joblib.load('model/gnv.joblib')

# Load the TfidfVectorizer object used during training
vectorizer = joblib.load('vectorizer/tfidf.joblib')
