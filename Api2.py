import sys
import pickle
from http.client import HTTPException

import nltk
import pandas as pd
import re

from fastapi import FastAPI
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import string
app = FastAPI()

with open("vectorizerTitleGenres.pkl", "rb") as f:
    tfidf_vectorizer = pickle.load(f)
with open("knn_modelTitleGenres.pkl", "rb") as f:
    model_knn = pickle.load(f)

data = pd.read_csv("C:\\Users\\bikti\\Fazafilms15.csv", low_memory=False)
english_stopwords = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def remove_punctuation(text):
    return "".join([ch if ch not in string.punctuation else ' ' for ch in text])

def remove_numbers(text):
    return ''.join([i if not i.isdigit() else ' ' for i in text])

def remove_multiple_spaces(text):
    return re.sub(r'\s+', ' ', text, flags=re.I)

other_symbols = '❯\xa0—«»'
def remove_othersymbol(text):
    return ''.join([ch if ch not in other_symbols else ' ' for ch in text])

def tokenize(text):
    t = word_tokenize(text)
    tokens = [token for token in t if token not in english_stopwords]
    return " ".join(tokens)

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize_text(text):
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in tokens]
    return " ".join(lemmatized_tokens)

def preprocess_movie_title(movie_name):
    movie_name = movie_name.lower()
    movie_name = remove_punctuation(movie_name)
    movie_name = remove_numbers(movie_name)
    movie_name = remove_othersymbol(movie_name)
    movie_name = remove_multiple_spaces(movie_name)
    movie_name = tokenize(movie_name)
    movie_name = lemmatize_text(movie_name)
    return movie_name


def find_similar_movies(movie_name, num_neighbors=10):
    processed_name = preprocess_movie_title(movie_name)
    movie_tfidf = tfidf_vectorizer.transform([processed_name])
    distances, indices = model_knn.kneighbors(movie_tfidf, n_neighbors=num_neighbors + 1)
    similar_movies = data.iloc[indices[0][1:]][['title', 'genres']].reset_index(drop=True)
    return similar_movies.to_dict(orient="records")

@app.get("/recommend")
def recommend_movies(title: str, num_neighbors: int = 10):
    if not title:
        raise HTTPException(status_code=400, detail="Ошибка")
    similar_movies = find_similar_movies(title, num_neighbors)
    return {"movies": similar_movies}
