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
