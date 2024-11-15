import streamlit as st
import requests

st.title("Рекомендательная система")

st.subheader("Топ 10 фильмов по контенту")
title = st.text_input("Введите название фильма")

if title:
    response = requests.get(f"http://127.0.0.1:8000/recommend", params={"title": title})
    response.raise_for_status()
    recommendations = response.json()["movies"]

    st.write("Похожие фильмы:")
    for i, movie in enumerate(recommendations, start=1):
        st.write(f"{i}. {movie['title']} - Жанры: {movie['genres']}")

