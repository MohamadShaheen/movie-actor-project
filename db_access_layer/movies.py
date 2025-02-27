from datetime import datetime
from sqlalchemy import extract
from fastapi import HTTPException

import database.mongodb_connection
from api_calls.tmdb_api import get_movie_poster
from database.models import Movie, MovieActor
from fastapi.encoders import jsonable_encoder
from database.mysql_connection import SessionLocal
from db_access_layer.actors import add_actor_general

session = SessionLocal()


def get_movies_ids():
    movies_ids = session.query(Movie.id).all()
    session.close()

    if not movies_ids:
        raise HTTPException(status_code=404, detail="Movies not found")

    return [movie[0] for movie in movies_ids]


def get_movies_titles():
    movies_titles = session.query(Movie.title).all()
    session.close()

    if not movies_titles:
        raise HTTPException(status_code=404, detail="Movies not found")

    return [title[0] for title in movies_titles]


def get_movie_by_id(movie_id: int):
    movie_db = session.query(Movie).filter(Movie.id == movie_id).first()
    session.close()

    if not movie_db:
        raise HTTPException(status_code=404, detail="Movie not found")

    return jsonable_encoder(movie_db)


def get_movie_by_title(movie_title: str):
    movie_db = session.query(Movie).filter(Movie.title.ilike(movie_title)).first()
    session.close()

    if not movie_db:
        raise HTTPException(status_code=404, detail="Movie not found")

    return jsonable_encoder(movie_db)


def get_movies_with_popularity_over(popularity: float):
    movies_db = session.query(Movie).filter(Movie.popularity > popularity).all()
    session.close()

    if not movies_db:
        raise HTTPException(status_code=404, detail="No movies found")

    return [{"id": movie.id, "title": movie.title, "popularity": movie.popularity} for movie in movies_db]


def get_movies_with_popularity_less(popularity: float):
    movies_db = session.query(Movie).filter(Movie.popularity < popularity).all()
    session.close()

    if not movies_db:
        raise HTTPException(status_code=404, detail="No movies found")

    return [{"id": movie.id, "title": movie.title, "popularity": movie.popularity} for movie in movies_db]


def get_movies_by_genre(genre: str):
    movies_db = session.query(Movie).filter(Movie.genres.contains(genre.lower().capitalize())).all()
    session.close()

    if not movies_db:
        raise HTTPException(status_code=404, detail="No movies found")

    return [{"id": movie.id, "title": movie.title, "genres": movie.genres.split(",")} for movie in movies_db]


def get_movies_released_after(year: int):
    movies_db = session.query(Movie).filter(extract("year", Movie.release_date) >= year).all()
    session.close()

    if not movies_db:
        raise HTTPException(status_code=404, detail="No movies found")

    return [{"id": movie.id, "title": movie.title, "release_date": movie.release_date} for movie in movies_db]


def get_movies_released_before(year: int):
    movies_db = session.query(Movie).filter(extract("year", Movie.release_date) <= year).all()
    session.close()

    if not movies_db:
        raise HTTPException(status_code=404, detail="No movies found")

    return [{"id": movie.id, "title": movie.title, "release_date": movie.release_date.strftime("%Y-%m-%d")} for movie in
            movies_db]


def get_movie_poster(movie_id: int):
    collection = database.mongodb_connection.database["movies_posters"]
    movie_db = collection.find_one({"_id": movie_id})

    if not movie_db:
        raise HTTPException(status_code=404, detail="Movie poster not found")

    return movie_db["image"]


def add_movies_poster(movies_ids):
    counter = 0
    collection = database.mongodb_connection.database["movies_posters"]

    for movie_id in movies_ids:
        movie_db = collection.find_one({"_id": movie_id})

        if not movie_db:
            mysql_movie_poster_path = session.query(Movie.poster_path).filter(Movie.id == movie_id).first()[0]
            counter += 1

            collection.insert_one({
                "_id": movie_id,
                "poster_path": mysql_movie_poster_path,
                "image": get_movie_poster(mysql_movie_poster_path)
            })

    return f"{counter} posters out of {len(movies_ids)} were added"


def add_movie_poster(movie_id: int):
    response = add_movies_poster([movie_id])

    if "0" in response.split():
        raise HTTPException(status_code=409, detail="Movie already exists")

    return f"Movie {movie_id} poster added successfully"


def add_movies(movies):
    counter = 0

    for movie in movies:
        movie_db = session.query(Movie).filter(Movie.id == movie["id"]).first()

        if not movie_db:
            counter += 1
            session.add(Movie(id=movie["id"], title=movie["title"], language=movie["language"],
                              popularity=movie["popularity"],
                              release_date=datetime.strptime(movie["release_date"], "%Y-%m-%d"),
                              adult=movie["adult"], genres=movie["genres"], overview=movie["overview"],
                              poster_path=movie["poster_path"]))
            session.commit()

        for actor in movie["actors"]:
            add_actor_general(actor)

            movie_actor_db = session.query(MovieActor).filter(MovieActor.movie_id == movie["id"],
                                                              MovieActor.actor_id == actor[
                                                                  "id"]).first()

            if not movie_actor_db:
                session.add(MovieActor(movie_id=movie["id"], actor_id=actor["id"]))

        session.commit()
        add_movies_poster([movie["id"]])

    session.close()
    return f"{counter} movies out of {len(movies)} were added"


def add_movie(movie):
    response = add_movies([movie])

    if "0" in response.split():
        raise HTTPException(status_code=409, detail="Movie already exists")

    add_movies_poster([movie["id"]])
    return f"Movie {movie["id"]} added successfully"


def delete_movies_poster(movies_ids):
    counter = 0
    collection = database.mongodb_connection.database["movies_posters"]

    for movie_id in movies_ids:
        result = collection.delete_one({"_id": movie_id})

        if result.deleted_count > 0:
            counter += 1

    return f"{counter} posters out of {len(movies_ids)} were deleted"


def delete_movie_poster(movie_id: int):
    response = delete_movies_poster([movie_id])

    if "0" in response.split():
        raise HTTPException(status_code=404, detail="Movie does not exist")

    return f"Movie {movie_id} poster deleted successfully"


def delete_movies(movies_ids):
    counter = 0

    for movie_id in movies_ids:
        movie_db = session.query(Movie).filter(Movie.id == movie_id).first()

        if movie_db:
            counter += 1

            session.delete(movie_db)
            session.commit()

    session.close()

    delete_movies_poster(movies_ids)
    return f"{counter} movies out of {len(movies_ids)} were deleted"


def delete_movie(movie_id: int):
    response = delete_movies([movie_id])

    if "0" in response.split():
        raise HTTPException(status_code=404, detail="Movie not found")

    delete_movies_poster([movie_id])
    return f"{movie_id} was deleted"
