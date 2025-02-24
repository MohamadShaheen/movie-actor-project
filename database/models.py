from sqlalchemy.orm import relationship
from mysql_connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(50))
    language = Column(String(5))
    popularity = Column(Float)
    release_date = Column(DateTime)
    adult = Column(Boolean)
    genres = Column(String(50))
    overview = Column(String(500))
    poster_path = Column(String(100))

    actors = relationship("Actor", secondary="movies_actors", back_populates="movies")


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(50))
    gender = Column(String(50))
    adult = Column(Boolean)
    popularity = Column(Float)
    profile_path = Column(String(100))

    movies = relationship("Movie", secondary="movies_actors", back_populates="actors")


class MovieActor(Base):
    __tablename__ = "movies_actors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete="CASCADE"), nullable=False)
    actor_id = Column(Integer, ForeignKey('actors.id', ondelete="CASCADE"), nullable=False)
