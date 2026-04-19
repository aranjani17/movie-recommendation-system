import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.data_preprocessing import merge_data
from src.model import build_model
from src.recommend import recommend_movies
from src.tmdb import get_movie_info, get_movies_info_bulk

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch · Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    background-color: #0a0a0f !important;
    color: #f0eee8 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.main { background-color: #0a0a0f !important; padding: 0 2rem; }

.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    background: radial-gradient(ellipse at 50% 0%, #1a0a2e 0%, #0a0a0f 70%);
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 2.5rem;
}
.hero h1 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 4.5rem !important;
    letter-spacing: 6px;
    color: #e8c96d !important;
    margin: 0 !important;
    text-shadow: 0 0 40px rgba(232,201,109,0.3);
}
.hero p {
    color: #8882a4;
    font-size: 1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.selected-card {
    display: flex;
    gap: 2rem;
    background: linear-gradient(135deg, #12111a, #1a1828);
    border: 1px solid #2a2840;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 2.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.selected-card img {
    width: 140px;
    height: 210px;
    object-fit: cover;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6);
}
.selected-card .info { flex: 1; }
.selected-card h2 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: #e8c96d;
    margin: 0 0 0.5rem;
    letter-spacing: 2px;
}
.selected-card .meta {
    color: #8882a4;
    font-size: 0.85rem;
    margin-bottom: 0.75rem;
}
.selected-card .overview {
    color: #ccc9e0;
    font-size: 0.92rem;
    line-height: 1.6;
}
.rating-badge {
    display: inline-block;
    background: #e8c96d;
    color: #0a0a0f;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 3px 12px;
    border-radius: 20px;
    margin-bottom: 0.75rem;
}

.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 4px;
    color: #e8c96d;
    border-left: 4px solid #e8c96d;
    padding-left: 1rem;
    margin-bottom: 1.5rem;
}

.movie-card {
    background: #12111a;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.movie-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(232,201,109,0.15);
    border-color: #e8c96d44;
}
.movie-card img {
    width: 100%;
    height: 260px;
    object-fit: cover;
}
.movie-card .no-poster {
    width: 100%;
    height: 260px;
    background: linear-gradient(135deg, #1a1828, #12111a);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
}
.movie-card .card-body { padding: 1rem; }
.movie-card .card-title {
    font-weight: 500;
    font-size: 0.9rem;
    color: #f0eee8;
    margin-bottom: 0.4rem;
    line-height: 1.3;
    min-height: 2.5rem;
}
.movie-card .card-meta { color: #8882a4; font-size: 0.78rem; margin-top: 2px; }
.stars { color: #e8c96d; font-size: 0.85rem; margin-bottom: 2px; }

.stSelectbox > div > div {
    background-color: #12111a !important;
    border: 1px solid #2a2840 !important;
    color: #f0eee8 !important;
    border-radius: 8px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #e8c96d, #c9a84c) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stProgress > div > div { background-color: #e8c96d !important; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎬 CineMatch</h1>
    <p>Discover your next favourite film</p>
</div>
""", unsafe_allow_html=True)

# ── Load data — stored in memory for entire session ──────────
@st.cache_resource(show_spinner=False)
def load():
    data = merge_data()
    popular = build_model(data)
    data = data[['userId', 'movieId', 'rating', 'title', 'genres']]
    movie_list = sorted(data['title'].unique().tolist())
    return data, popular, movie_list

# Show progress bar only on very first load
if 'loaded' not in st.session_state:
    bar = st.progress(0, text="🎬 Loading cinema database...")
    data, popular_movies, movie_list = load()
    bar.progress(100, text="✅ Ready!")
    bar.empty()
    st.session_state['loaded'] = True
else:
    data, popular_movies, movie_list = load()

# ── TMDB cache per title ─────────────────────────────────────
@st.cache_data(show_spinner=False)
def fetch_info(title):
    return get_movie_info(title)

@st.cache_data(show_spinner=False)
def fetch_bulk(titles_tuple):
    return get_movies_info_bulk(list(titles_tuple))

# ── Search bar ───────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    selected_movie = st.selectbox(
        "Search a movie you like",
        movie_list,
        label_visibility="collapsed"
    )
with col2:
    recommend_btn = st.button("Find Similar →")

# ── Selected movie info card ─────────────────────────────────
if selected_movie:
    info = fetch_info(selected_movie)
    avg_r = popular_movies[popular_movies['title'] == selected_movie]['avg_rating']
    user_rating = f"{avg_r.values[0]:.1f} / 5.0" if not avg_r.empty else "N/A"

    poster_html = (
        f'<img src="{info["poster"]}" alt="poster"/>'
        if info["poster"] else
        '<div style="width:140px;height:210px;background:#1a1828;border-radius:10px;'
        'display:flex;align-items:center;justify-content:center;font-size:3rem;">🎬</div>'
    )

    st.markdown(f"""
    <div class="selected-card">
        {poster_html}
        <div class="info">
            <h2>{selected_movie}</h2>
            <div class="meta">📅 {info['year']} &nbsp;|&nbsp; ⭐ TMDB: {info['tmdb_rating']}/10</div>
            <div class="rating-badge">★ User Rating: {user_rating}</div>
            <div class="overview">
                {info['overview'][:300]}{'...' if len(info['overview']) > 300 else ''}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Recommendation grid ──────────────────────────────────────
if recommend_btn:
    results = recommend_movies(selected_movie, data, popular_movies)

    with st.spinner("Fetching posters..."):
        all_info = fetch_bulk(tuple(results))

    st.markdown('<div class="section-title">RECOMMENDED FOR YOU</div>', unsafe_allow_html=True)

    cols = st.columns(6)
    for i, movie in enumerate(results):
        info = all_info.get(movie, {"poster": None, "tmdb_rating": 0, "year": ""})

        avg_r = popular_movies[popular_movies['title'] == movie]['avg_rating']
        rating = f"{avg_r.values[0]:.1f}" if not avg_r.empty else "N/A"

        num_r = popular_movies[popular_movies['title'] == movie]['num_ratings']
        count = f"{int(num_r.values[0])}" if not num_r.empty else ""

        stars_count = int(round(avg_r.values[0])) if not avg_r.empty else 0
        stars_html = "★" * stars_count + "☆" * (5 - stars_count)

        poster_html = (
            f'<img src="{info["poster"]}" alt="{movie}"/>'
            if info.get("poster") else
            '<div class="no-poster">🎬</div>'
        )

        with cols[i % 6]:
            st.markdown(f"""
            <div class="movie-card">
                {poster_html}
                <div class="card-body">
                    <div class="card-title">{movie}</div>
                    <div class="stars">{stars_html}</div>
                    <div class="card-meta">⭐ {rating}/5 · {count} ratings</div>
                    <div class="card-meta">🎬 TMDB: {info['tmdb_rating']}/10</div>
                </div>
            </div>
            """, unsafe_allow_html=True)