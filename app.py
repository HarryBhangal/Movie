import streamlit as st
import pickle
import pandas as pd

# Load the data
movies = pickle.load(open('movie.pkl', 'rb'))  # This should be a DataFrame
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def recommend(movie_title):
    # Get the index of the selected movie
    movie_index = movies[movies['title'] == movie_title].index[0]

    # Get similarity scores
    distances = similarity[movie_index]

    # Get top 5 similar movies (excluding itself)
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies

# Streamlit UI
st.title("🎬 What You Wanna Watch?")

# Movie selection box
option = st.selectbox(
    'Which movie have you watched?',
    movies['title'].values
)

# Recommend button
if st.button('Recommend'):
    recommendations = recommend(option)
    st.subheader("Recommended Movies:")
    for i in recommendations:
        st.write("👉", i)
