

import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title="Movie Engine", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }

    .block-container {
        padding-top: 1rem;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}

    .stSelectbox label p {
        color: red !important;
        font-weight: bold;
    }

    div[data-baseweb="select"] svg {
        fill: #00d2ff !important;
    }

    .movie-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 12px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: 0.3s;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        max-width :330px;
        margin:auto;
    }

    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.6);
        border: 1px solid #00d2ff;
    }

    .movie-title {
        color: #e0e0e0;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 8px;
        min-height: 60px;
        line-height: 1.3;
        word-wrap: break-word;
    }

    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 25px;
        font-weight: bold;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    from config import API_KEY
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        pass

    return "https://via.placeholder.com/500x750?text=No+Image"


def recommended(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)

    names = []
    posters = []

    for i in distances[1:5]:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


movies = pd.DataFrame(pickle.load(open('movies_dict.pkl', 'rb')))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    selected_movie = st.selectbox("Select a movie", movies['title'].values)
    btn = st.button("Show Recommendations")

st.write("---")

if btn:
    with st.spinner("🎬 Loading movies for you..."):
        names, posters = recommended(selected_movie)

    cols = st.columns(4)

    for i in range(4):
        with cols[i]:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{posters[i]}" 
                    style="width:100%; max-height:320px; object-fit:contain; border-radius:25px;">
                    <div class="movie-title">{names[i]}</div>
                </div>
            """, unsafe_allow_html=True)