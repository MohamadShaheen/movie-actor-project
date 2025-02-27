import re
from typing import List
from db_access_layer import movies
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/movies-ids/")
async def get_movies_ids():
    try:
        response = movies.get_movies_ids()
        return response
    except HTTPException as err:
        raise err


@router.get("/movies-titles/")
async def get_movies_titles():
    try:
        response = movies.get_movies_titles()
        return response
    except HTTPException as err:
        raise err


@router.get("/movie-by-id/")
async def get_movie_by_id(movie_id: int):
    try:
        response = movies.get_movie_by_id(movie_id)
        return response
    except HTTPException as err:
        raise err


@router.get("/movie-by-title/")
async def get_movie_by_title(movie_title: str):
    try:
        response = movies.get_movie_by_title(movie_title)
        return response
    except HTTPException as err:
        raise err


@router.get("/movies-with-popularity-over/")
async def get_movies_with_popularity_over(popularity: float):
    try:
        response = movies.get_movies_with_popularity_over(popularity)
        return response
    except HTTPException as err:
        raise err


@router.get("/movies-with-popularity-less/")
async def get_movies_with_popularity_less(popularity: float):
    try:
        response = movies.get_movies_with_popularity_less(popularity)
        return response
    except HTTPException as err:
        raise err


@router.get("/movies-by-genre/")
async def get_movies_by_genre(genre: str):
    try:
        response = movies.get_movies_by_genre(genre)
        return response
    except HTTPException as err:
        raise err


@router.get("/movies-released-after/")
async def get_movies_released_after(year: int):
    try:
        response = movies.get_movies_released_after(year)
        return response
    except HTTPException as err:
        raise err


@router.get("/movies-released-before/")
async def get_movies_released_before(year: int):
    try:
        response = movies.get_movies_released_before(year)
        return response
    except HTTPException as err:
        raise err


@router.post("/add-movies/")
async def add_movies(movies_list: List[dict]):
    try:
        response = movies.add_movies(movies_list)
        return response
    except HTTPException as err:
        raise err


@router.post("/add-movie/")
async def add_movie(id: int, title: str, language: str, popularity: float, release_date: str, adult: bool, genres: str,
                    overview: str, poster_path: str):
    try:
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", release_date):
            raise HTTPException(status_code=400, detail="Invalid date format. Use dd-mm-yyyy")

        if not re.match(r"^[A-Za-z]+(,[A-Za-z]+)*$", genres):
            raise HTTPException(status_code=400,
                                detail="Invalid genres format. Use comma-separated words like 'Action,Comedy'")

        response = movies.add_movie(
            {"id": id, "title": title, "language": language, "popularity": popularity, "release_date": release_date,
             "adult": adult, "genres": genres, "overview": overview, "poster_path": poster_path, "actors": []})
        return response
    except HTTPException as err:
        raise err


@router.delete("/delete-movies/")
async def delete_movies(movies_ids: List[int]):
    try:
        response = movies.delete_movies(movies_ids)
        return response
    except HTTPException as err:
        raise err


@router.delete("/delete-movie/")
async def delete_movie(movie_id: int):
    try:
        response = movies.delete_movies(movie_id)
        return response
    except HTTPException as err:
        raise err
