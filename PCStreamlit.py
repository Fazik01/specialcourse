import streamlit as st
import requests


def send_request_top10():
    response = requests.get("http://localhost:8000/movie/top10")
    return response.json()

def send_request_top10genre(genre):
    response = requests.get(f"http://localhost:8000/movie/top10genre?genre={genre}")
    return response.json()

def send_request_top10rec(title):
    response = requests.get(f"http://localhost:8000/movie/top10rec?title={title}")
    return response.json()

def send_request_allGenres():
    response = requests.get("http://localhost:8000/genre")
    return response.json()

st.write("""
# Справка
Функционал программы:
- **Топ 10 популярных фильмов**: выводит информацию о 10 наиболее высокооцененных фильмах.
- **Топ 10 фильмов по жанру**: введите жанр, и программа выдаст информацию о 10 наиболее высокооцененных фильмах в данном жанре.
- **Топ 10 фильмов по контенту**: введите название фильма, и программа выдаст информацию о 10 похожих произведений.""")

st.title("Рекомендательная система")

st.subheader("Топ 10 популярных фильмов")
top10_data = send_request_top10()
for i, movie in enumerate(top10_data, start=1):
    st.write(f"{i}. {movie['title']} — Оценка: {movie['w_score']}")

st.subheader("Топ 10 фильмов по жанру")
options = send_request_allGenres()
genre = st.selectbox('Выберите жанр', options)
if genre:
    top10genre_data = send_request_top10genre(genre)
    st.write(f"Топ 10 фильмов по жанру {genre}:")
    for i, movie in enumerate(top10genre_data, start=1):
        st.write(f"{i}. {movie['title']} — Оценка: {movie['w_score']}")

st.subheader("Топ 10 фильмов по контенту")
title = st.text_input("Введите название фильма")
if title:
    top10rec_data = send_request_top10rec(title)
    st.write("Похожие фильмы:")
    for i, movie in enumerate(top10rec_data, start=1):
        st.write(f"{i}. {movie['Фильм']}")

