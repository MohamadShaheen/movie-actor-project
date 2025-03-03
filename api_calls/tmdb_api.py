import os
from io import BytesIO
import requests
from bson import Binary
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

    genres = get_genres()
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
                "genres": ','.join([genres[genre_id] for genre_id in movie["genre_ids"]]),
                "overview": movie["overview"],
                "poster_path": movie["poster_path"],
                "actors": get_actors(movie["id"]),
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


def get_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    response = requests.get(url, headers=headers).json()["genres"]
    genres = {}

    for genre in response:
        genres[genre["id"]] = genre["name"]

    return genres


def get_movie_poster(movie_poster_path: str):
    if movie_poster_path == "":
        return None

    url = "https://image.tmdb.org/t/p/original" + movie_poster_path

    response = requests.get(url)

    if response.status_code == 200:
        return Binary(response.content)
    else:
        return None
