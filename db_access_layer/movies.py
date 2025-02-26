import json
from datetime import datetime
from sqlalchemy import extract
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from database.mysql_connection import SessionLocal
from database.models import Movie, Actor, MovieActor


class MovieInteractor:
    def __init__(self):
        self.session = SessionLocal()

    def get_movies_ids(self):
        movies_ids = self.session.query(Movie.id).all()

        if not movies_ids:
            self.session.close()
            raise HTTPException(status_code=404, detail="Movies not found")

        return [movie[0] for movie in movies_ids]

    def get_movies_titles(self):
        movies_titles = self.session.query(Movie.title).all()

        if not movies_titles:
            self.session.close()
            raise HTTPException(status_code=404, detail="Movies not found")

        return [title[0] for title in movies_titles]

    def get_movie_by_id(self, movie_id: int):
        movie_db = self.session.query(Movie).filter(Movie.id == movie_id).first()

        if not movie_db:
            self.session.close()
            raise HTTPException(status_code=404, detail="Movie not found")

        return jsonable_encoder(movie_db)

    def get_movie_by_title(self, movie_title: str):
        movie_db = self.session.query(Movie).filter(Movie.title.ilike(movie_title)).first()

        if not movie_db:
            self.session.close()
            raise HTTPException(status_code=404, detail="Movie not found")

        return jsonable_encoder(movie_db)

    def get_movies_with_popularity_over(self, popularity: float):
        movies_db = self.session.query(Movie).filter(Movie.popularity > popularity).all()

        movies = []

        for movie in movies_db:
            movies.append({"id": movie.id, "title": movie.title, "popularity": movie.popularity})

        return movies

    def get_movies_with_popularity_less(self, popularity: float):
        movies_db = self.session.query(Movie).filter(Movie.popularity < popularity).all()

        movies = []

        for movie in movies_db:
            movies.append({"id": movie.id, "title": movie.title, "popularity": movie.popularity})

        return movies

    def get_movies_by_genre(self, genre: str):
        movies_db = self.session.query(Movie).filter(Movie.genres.contains(genre.lower().capitalize())).all()

        movies = []

        for movie in movies_db:
            movies.append({"id": movie.id, "title": movie.title, "genres": movie.genres.split(",")})

        return movies

    def get_movies_released_after(self, year: int):
        movies_db = self.session.query(Movie).filter(extract("year", Movie.release_date) >= year).all()

        movies = []

        for movie in movies_db:
            movies.append({"id": movie.id, "title": movie.title, "release_date": movie.release_date})

        return movies

    def get_movies_released_before(self, year: int):
        movies_db = self.session.query(Movie).filter(extract("year", Movie.release_date) <= year).all()

        movies = []

        for movie in movies_db:
            movies.append(
                {"id": movie.id, "title": movie.title, "release_date": movie.release_date.strftime("%Y-%m-%d")})

        return movies

    def add_movie(self, movie):
        response = self.add_movies([movie])

        if "0" in response.split():
            raise HTTPException(status_code=409, detail="Movie already exists")

        return f"Movie {movie["id"]} added successfully"

    def add_movies(self, movies):
        counter = 0

        for movie in movies:
            movie_db = self.session.query(Movie).filter(Movie.id == movie["id"]).first()

            if not movie_db:
                counter += 1
                self.session.add(Movie(id=movie["id"], title=movie["title"], language=movie["language"],
                                       popularity=movie["popularity"],
                                       release_date=datetime.strptime(movie["release_date"], "%Y-%m-%d"),
                                       adult=movie["adult"], genres=movie["genres"], overview=movie["overview"],
                                       poster_path=movie["poster_path"]))
                self.session.commit()

            for actor in movie["actors"]:
                actor_db = self.session.query(Actor).filter(Actor.id == actor["id"]).first()

                if not actor_db:
                    self.session.add(Actor(id=actor["id"], name=actor["name"],
                                           gender=actor["gender"], adult=actor["adult"],
                                           popularity=actor["popularity"], profile_path=actor["profile_path"]))

                    self.session.commit()

                movie_actor_db = self.session.query(MovieActor).filter(MovieActor.movie_id == movie["id"],
                                                                       MovieActor.actor_id == actor[
                                                                           "id"]).first()

                if not movie_actor_db:
                    self.session.add(MovieActor(movie_id=movie["id"], actor_id=actor["id"]))

            self.session.commit()
            self.session.close()

        return f"{counter} movies out of {len(movies)} were added"

    def delete_movie(self, movie_id):
        response = self.delete_movies([movie_id])

        if "0" in response.split():
            raise HTTPException(status_code=404, detail="Movie not found")

        return f"{movie_id} was deleted"

    def delete_movies(self, movies_ids):
        counter = 0

        for movie_id in movies_ids:
            movie_db = self.session.query(Movie).filter(Movie.id == movie_id).first()

            if movie_db:
                counter += 1

                self.session.delete(movie_db)
                self.session.commit()
                self.session.close()

        return f"{counter} movies out of {len(movies_ids)} were deleted"
