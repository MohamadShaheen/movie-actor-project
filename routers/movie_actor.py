from db_access_layer import movie_actor
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/movie-actors-by-id/")
async def get_movie_actors_by_id(movie_id: int):
    try:
        response = movie_actor.get_movie_actors_by_id(movie_id)
        return response
    except HTTPException as err:
        raise err


@router.get("/movie-actors-by-name/")
async def get_movie_actors_by_name(movie_title: str):
    try:
        response = movie_actor.get_movie_actors_by_name(movie_title)
        return response
    except HTTPException as err:
        raise err


@router.get("/actor-movies-by-id/")
async def get_actor_movies_by_id(actor_id: int):
    try:
        response = movie_actor.get_actor_movies_by_id(actor_id)
        return response
    except HTTPException as err:
        raise err


@router.get("/actor-movies-by-name/")
async def get_actor_movies_by_name(actor_name: str):
    try:
        response = movie_actor.get_actor_movies_by_name(actor_name)
        return response
    except HTTPException as err:
        raise err


@router.post("/add-movie-actor/")
async def add_movie_actor(movie_id: int, actor_id: int):
    try:
        response = movie_actor.add_movie_actor(movie_id, actor_id)
        return response
    except HTTPException as err:
        raise err


@router.delete("/delete-movie-actor/")
async def delete_movie_actor(movie_id: int, actor_id: int):
    try:
        response = movie_actor.delete_movie_actor(movie_id, actor_id)
        return response
    except HTTPException as err:
        raise err
