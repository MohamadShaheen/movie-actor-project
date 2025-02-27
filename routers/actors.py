from typing import List

from fastapi import APIRouter, HTTPException

from database.models import Actor
from db_access_layer import actors

router = APIRouter()


@router.get("/actors-ids/")
async def get_actors_ids():
    try:
        response = actors.get_actors_ids()
        return response
    except HTTPException as err:
        raise err


@router.get("/actors-names/")
async def get_actors_names():
    try:
        response = actors.get_actors_names()
        return response
    except HTTPException as err:
        raise err


@router.get("/actor-by-id/")
async def get_actor_by_id(actor_id: int):
    try:
        response = actors.get_actor_by_id(actor_id)
        return response
    except HTTPException as err:
        raise err


@router.get("/actor-by-name/")
async def get_actor_by_name(actor_name: str):
    try:
        response = actors.get_actor_by_name(actor_name)
        return response
    except HTTPException as err:
        raise err


@router.get("/actor-by-gender/")
async def get_actor_by_gender(gender: str):
    try:
        response = actors.get_actor_by_gender(gender)
        return response
    except HTTPException as err:
        raise err


@router.get("/actor-with-popularity-over/")
async def get_actor_with_popularity_over(popularity: float):
    try:
        response = actors.get_actor_with_popularity_over(popularity)
        return response
    except HTTPException as err:
        raise err


@router.get("/actor-with-popularity-less/")
async def get_actor_with_popularity_less(popularity: float):
    try:
        response = actors.get_actor_with_popularity_less(popularity)
        return response
    except HTTPException as err:
        raise err


@router.post("/add-actors/")
async def add_actor(actors_list: List[dict]):
    try:
        response = actors.add_actors(actors_list)
        return response
    except HTTPException as err:
        raise err


@router.post("/add-actor/")
async def add_actor(id: int, name: str, gender: str, adult: bool, popularity: float, profile_path: str):
    try:
        if gender.lower() != "male" and gender.lower() != "female":
            raise HTTPException(status_code=400, detail="Gender must be either male or female")

        response = actors.add_actor({
            "id": id,
            "name": name,
            "gender": gender,
            "adult": adult,
            "popularity": popularity,
            "profile_path": profile_path
        })
        return response
    except HTTPException as err:
        raise err


@router.delete("/delete-actors/")
async def delete_actors(actors_ids: List[int]):
    try:
        response = actors.delete_actors(actors_ids)
        return response
    except HTTPException as err:
        raise err


@router.delete("/delete-actor/")
async def delete_actor(actor_id: int):
    try:
        response = actors.delete_actor(actor_id)
        return response
    except HTTPException as err:
        raise err
