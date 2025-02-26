from fastapi import HTTPException
from database.mysql_connection import SessionLocal
from database.models import MovieActor, Actor, Movie

session = SessionLocal()


def get_actors_general(movie_actor_db):
    actors_ids = [actor[0] for actor in movie_actor_db]

    actors = []
    for actor_id in actors_ids:
        actor = session.query(Actor).filter(Actor.id == actor_id).first()

        if actor:
            actors.append({"id": actor.id, "name": actor.name})

    session.close()
    return actors


def get_movies_general(movie_actor_db):
    movies_id = [movie[0] for movie in movie_actor_db]

    movies = []
    for movie_id in movies_id:
        movie = session.query(Movie).filter(Movie.id == movie_id).first()

        if movie:
            movies.append({"id": movie.id, "title": movie.title})

    session.close()
    return movies


def get_movie_actors_by_id(movie_id: int):
    movie_actor_db = session.query(MovieActor.actor_id).filter(MovieActor.movie_id == movie_id).all()

    if not movie_actor_db:
        raise HTTPException(status_code=422, detail="Movie id is not found")

    return get_actors_general(movie_actor_db)


def get_movie_actors_by_name(movie_title: str):
    movie_db = session.query(Movie).filter(Movie.title.ilike(movie_title)).first()
    movie_actor_db = session.query(MovieActor.actor_id).filter(MovieActor.movie_id == movie_db.id).all()

    if not movie_actor_db:
        raise HTTPException(status_code=422, detail="Movie title is not found")

    return get_actors_general(movie_actor_db)


def get_actor_movies_by_id(actor_id: int):
    movie_actor_db = session.query(MovieActor.movie_id).filter(MovieActor.actor_id == actor_id).all()

    if not movie_actor_db:
        raise HTTPException(status_code=422, detail="Movie id is not found")

    return get_movies_general(movie_actor_db)


def get_actor_movies_by_name(actor_name: str):
    actor_db = session.query(Actor).filter(Actor.name.ilike(actor_name)).first()
    movie_actor_db = session.query(MovieActor.movie_id).filter(MovieActor.actor_id == actor_db.id).all()

    if not movie_actor_db:
        raise HTTPException(status_code=422, detail="Movie title is not found")

    return get_movies_general(movie_actor_db)


def add_movie_actor(movie_id, actor_id):
    movie_db = session.query(Movie).filter(Movie.id == movie_id).first()

    if not movie_db:
        session.close()
        raise HTTPException(status_code=422, detail="Movie id not found")

    actor_db = session.query(Actor).filter(Actor.id == actor_id).first()

    if not actor_db:
        session.close()
        raise HTTPException(status_code=422, detail="Actor id not found")

    session.add(MovieActor(movie_id=movie_id, actor_id=actor_id))
    session.commit()
    session.close()

    return f"{actor_id} added to {movie_id}"


def delete_movie_actor(movie_id, actor_id):
    movie_actor_db = session.query(MovieActor).filter(MovieActor.movie_id == movie_id,
                                                      MovieActor.actor_id == actor_id).first()

    if not movie_actor_db:
        session.close()
        raise HTTPException(status_code=422, detail=f"Actor {actor_id} is not related to the movie {movie_id}")

    session.delete(movie_actor_db)
    session.commit()
    session.close()

    return f"{actor_id} added to {movie_id}"
