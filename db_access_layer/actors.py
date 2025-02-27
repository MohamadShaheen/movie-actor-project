from fastapi import HTTPException
from database.models import Actor
from fastapi.encoders import jsonable_encoder
from database.mysql_connection import SessionLocal

session = SessionLocal()


def get_actors_ids():
    actors_ids = session.query(Actor.id).all()

    if not actors_ids:
        session.close()
        raise HTTPException(status_code=404, detail="No actors found")

    session.close()
    return [actor[0] for actor in actors_ids]


def get_actors_names():
    actors_names = session.query(Actor.name).all()

    if not actors_names:
        session.close()
        raise HTTPException(status_code=404, detail="No actors found")

    session.close()
    return [actor[0] for actor in actors_names]


def get_actor_by_id(actor_id: int):
    actor_db = session.query(Actor).filter(Actor.id == actor_id).first()

    if not actor_db:
        session.close()
        raise HTTPException(status_code=404, detail="No actor found")

    session.close()
    return jsonable_encoder(actor_db)


def get_actor_by_name(actor_name: str):
    actor_db = session.query(Actor).filter(Actor.name.ilike(actor_name)).first()

    if not actor_db:
        session.close()
        raise HTTPException(status_code=404, detail="No actor found")

    session.close()
    return jsonable_encoder(actor_db)


def get_actor_by_gender(gender: str):
    if gender.lower() != "male" and gender.lower() != "female":
        session.close()
        raise HTTPException(status_code=422, detail="Invalid gender value. Must be 'male' or 'female'")

    actors_db = session.query(Actor).filter(Actor.gender.ilike(gender)).all()

    if not actors_db:
        session.close()
        raise HTTPException(status_code=404, detail="No actor found")

    session.close()
    return [{"id": actor.id, "name": actor.name} for actor in actors_db]


def get_actor_with_popularity_over(popularity: float):
    actors_db = session.query(Actor).filter(Actor.popularity >= popularity).all()

    if not actors_db:
        session.close()
        raise HTTPException(status_code=404, detail="No actor found")

    session.close()
    return [{"id": actor.id, "name": actor.name, "popularity": actor.popularity} for actor in actors_db]


def get_actor_with_popularity_less(popularity: float):
    actors_db = session.query(Actor).filter(Actor.popularity <= popularity).all()

    if not actors_db:
        session.close()
        raise HTTPException(status_code=404, detail="No actor found")

    session.close()
    return [{"id": actor.id, "name": actor.name, "popularity": actor.popularity} for actor in actors_db]


def add_actor_general(actor):
    actor_db = session.query(Actor).filter(Actor.id == actor["id"]).first()

    if not actor_db:
        session.add(Actor(id=actor["id"], name=actor["name"], gender=actor["gender"],
                          adult=actor["adult"], popularity=actor["popularity"], profile_path=actor["profile_path"]))
        session.commit()
        return True

    return False


def add_actors(actors):
    counter = 0

    for actor in actors:
        if add_actor_general(actor):
            counter += 1

    session.close()
    return f"{counter} actors added"


def add_actor(actor):
    response = add_actors([actor])

    if "0" in response.split():
        raise HTTPException(status_code=409, detail="Actor already exists")

    return f"Actor {actor["id"]} added successfully"


def delete_actors(actors_ids):
    counter = 0

    for actor_id in actors_ids:
        actor_db = session.query(Actor).filter(Actor.id == actor_id).first()

        if actor_db:
            counter += 1

            session.delete(actor_db)
            session.commit()

    session.close()
    return f"{counter} actors out of {len(actors_ids)} were deleted"


def delete_actor(actor_id):
    response = delete_actors([actor_id])

    if "0" in response.split():
        raise HTTPException(status_code=404, detail="Actor not found")

    return f"{actor_id} was deleted"
