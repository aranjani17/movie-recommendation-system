import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

TMDB_API_KEY = "9f0de0adb9ce46bf4ac3a900de1ddc5d"  # <-- your key here
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"

def clean_title(title):
    return re.sub(r'\s*\(\d{4}\)', '', title).strip()

def get_movie_info(title):
    clean = clean_title(title)
    try:
        res = requests.get(
            f"{BASE_URL}/search/movie",
            params={"api_key": TMDB_API_KEY, "query": clean},
            timeout=4
        )
        results = res.json().get("results", [])
        if results:
            m = results[0]
            return {
                "title": title,
                "poster": f"{IMG_BASE}{m['poster_path']}" if m.get('poster_path') else None,
                "overview": m.get("overview", "No description available."),
                "tmdb_rating": round(m.get("vote_average", 0), 1),
                "year": m.get("release_date", "")[:4]
            }
    except Exception:
        pass
    return {"title": title, "poster": None, "overview": "", "tmdb_rating": 0, "year": ""}

def get_movies_info_bulk(titles):
    """Fetch all movies in parallel — much faster than one by one"""
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_title = {executor.submit(get_movie_info, t): t for t in titles}
        for future in as_completed(future_to_title):
            data = future.result()
            results[data["title"]] = data
    return results