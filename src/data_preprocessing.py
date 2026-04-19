import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def merge_data():
    movies_path = os.path.join(BASE_DIR, 'data', 'movies.csv')
    ratings_path = os.path.join(BASE_DIR, 'data', 'ratings.csv')

    # Load only needed columns — much faster
    movies = pd.read_csv(movies_path, usecols=['movieId', 'title', 'genres'])
    ratings = pd.read_csv(ratings_path, usecols=['userId', 'movieId', 'rating'],
                          dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})

    data = pd.merge(ratings, movies, on='movieId')
    return data