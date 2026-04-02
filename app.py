
import streamlit as st
import pickle
import requests
from PIL import Image
from io import BytesIO

# Load saved model files
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

TMDB_API_KEY = "a02686f33ba18408b7316f531873655a"  # Replaced with your API key

def fetch_poster(title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": title}
    try:
        res = requests.get(url, params=params, timeout=5).json()
        if res['results'] and res['results'][0].get('poster_path'):
            return "https://image.tmdb.org/t/p/w300" + res['results'][0]['poster_path']
    except:
        return None

def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[idx])),
                           key=lambda x: x[1], reverse=True)[1:11]
    return [movies.iloc[i[0]].title for i in distances]

# Website Layout
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎬 Movie & TV Show Recommendation System")
st.markdown("Select a movie and get **Top 10 similar recommendations** with posters!")

selected = st.selectbox("Choose a movie:", movies['title'].values)

if st.button("Recommend 🎯"):
    titles = recommend(selected)
    st.subheader("Top 10 Recommendations:")
    cols = st.columns(5)
    for i, title in enumerate(titles):
        with cols[i % 5]:
            poster = fetch_poster(title)
            if poster:
                st.image(poster, width=180) # Fixed deprecated parameter
                st.caption(f"**{i+1}. {title}**")
