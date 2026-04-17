import requests
import re

TMDB_API_KEY = "9f0de0adb9ce46bf4ac3a900de1ddc5d"   # <-- Paste your key here
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"

def clean_title(title):
    # Remove year like "(1995)" from title
    return re.sub(r'\s*\(\d{4}\)', '', title).strip()

def get_movie_info(title):
    clean = clean_title(title)
    try:
        url = f"{BASE_URL}/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": clean}
        res = requests.get(url, params=params, timeout=5)
        results = res.json().get("results", [])
        if results:
            movie = results[0]
            poster = f"{IMG_BASE}{movie['poster_path']}" if movie.get('poster_path') else None
            return {
                "poster": poster,
                "overview": movie.get("overview", "No description available."),
                "tmdb_rating": round(movie.get("vote_average", 0), 1),
                "year": movie.get("release_date", "")[:4]
            }
    except Exception:
        pass
    return {"poster": None, "overview": "", "tmdb_rating": 0, "year": ""}