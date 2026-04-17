def recommend_movies(selected_movie, data, popular_movies):
    selected_info = data[data['title'] == selected_movie][['title', 'genres']].drop_duplicates()
    if selected_info.empty:
        return popular_movies['title'].head(6).tolist()
    genre_list = selected_info.iloc[0]['genres'].split('|')
    all_movies = data[['title', 'genres']].drop_duplicates()
    all_movies = all_movies[all_movies['title'] != selected_movie]
    similar = all_movies[all_movies['genres'].apply(lambda g: any(x in g for x in genre_list))]
    result = similar.merge(popular_movies, on='title').sort_values('avg_rating', ascending=False)
    return result['title'].head(6).tolist()