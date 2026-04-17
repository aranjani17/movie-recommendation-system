def build_model(data):
    movie_stats = data.groupby('title').agg(
        avg_rating=('rating', 'mean'),
        num_ratings=('rating', 'count')
    ).reset_index()
    popular_movies = movie_stats[movie_stats['num_ratings'] >= 10]
    popular_movies = popular_movies.sort_values('avg_rating', ascending=False)
    return popular_movies