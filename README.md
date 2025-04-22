# 🎬 Movie Recommender System

A simple content-based movie recommender system built using Python. This project suggests similar movies based on user input using natural language features such as movie overviews, genres, and keywords.

---

## 🔧 Built With

- **Python**
- **Pandas** – for data manipulation and preprocessing
- **Scikit-learn** – for vectorization and similarity calculation
- **Pickle** – for saving and loading the trained model

---

## 🚀 Features

- ✅ Recommend similar movies based on a selected title
- ✅ Uses cosine similarity for content-based filtering
- ✅ Lightweight and easy to integrate into web apps or APIs

---

## 📁 Dataset

This project uses a subset of the **TMDB 5000 Movies Dataset** (or any similar dataset with relevant columns like title, genres, overview, keywords, etc.).

---

## 🧠 How It Works

1. Combine textual metadata such as:
   - Overview
   - Genres
   - Keywords
2. Convert this combined text into vectors using `CountVectorizer` or `TfidfVectorizer`
3. Compute **cosine similarity** between all movies
4. Recommend the top N similar movies for any selected title

---
