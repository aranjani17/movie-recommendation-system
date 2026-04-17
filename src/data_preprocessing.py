import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def merge_data():
    movies_path = os.path.join(BASE_DIR, 'data', 'movies.csv')
    ratings_path = os.path.join(BASE_DIR, 'data', 'ratings.csv')
    movies = pd.read_csv(movies_path)
    ratings = pd.read_csv(ratings_path)
    data = pd.merge(ratings, movies, on='movieId')
    return data