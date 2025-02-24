import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_access_token = os.getenv("API_ACCESS_TOKEN")

headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + api_access_token
}


def get_popular_movies(pages: int):
    if pages <= 0:
        print("Invalid input - pages number must be greater than zero")
        return []
    elif pages > 20:
        print("Invalid input - pages number must be less than 20")
        return []

    # Base URL
    url = f"https://api.themoviedb.org/3/movie/popular?language=en-US&page="

    # Movies List
    movies = []

    # Iterate through the given number of pages
    for page in range(1, pages + 1):
        # Provide the current page number for proper request
        response = requests.get(url + str(page), headers=headers).json()["results"]

        # Movies list in the current page
        movies_per_page = []

        for movie in response:
            movies_per_page.append({
                "id": movie["id"],
                "title": movie["original_title"],
                "language": movie["original_language"],
                "popularity": movie["popularity"],
                "release_date": movie["release_date"],
                "adult": movie["adult"],
                "genres": ','.join([str(genre_id) for genre_id in movie["genre_ids"]]),
                "overview": movie["overview"],
                "poster_path": movie["poster_path"],
            })

        movies.extend(movies_per_page)

    return movies


def get_actors(movie_id: int):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"

    response = requests.get(url, headers=headers).json()["cast"]

    # Actors list
    actors = []

    for actor in response:
        actors.append({
            "id": actor["id"],
            "name": actor["name"],
            "gender": "male" if actor["gender"] == 2 else "female",
            "adult": actor["adult"],
            "popularity": actor["popularity"],
            "profile_path": actor["profile_path"]
        })

    return actors
