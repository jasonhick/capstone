import datetime
import random

from flask import Flask

from .common import get_logger
from .config import Config
from .database import DBTransaction, db
from .models import Actor, Movie

logger = get_logger()

# Sample data
ACTORS = [
    {
        "name": "Emma Thompson",
        "age": 62,
        "gender": "Female",
        "birthdate": datetime.date(1959, 4, 15),
    },
    {
        "name": "Tom Hanks",
        "age": 65,
        "gender": "Male",
        "birthdate": datetime.date(1956, 7, 9),
    },
    {
        "name": "Viola Davis",
        "age": 56,
        "gender": "Female",
        "birthdate": datetime.date(1965, 8, 11),
    },
    {
        "name": "Idris Elba",
        "age": 49,
        "gender": "Male",
        "birthdate": datetime.date(1972, 9, 6),
    },
    {
        "name": "Meryl Streep",
        "age": 72,
        "gender": "Female",
        "birthdate": datetime.date(1949, 6, 22),
    },
    {
        "name": "Denzel Washington",
        "age": 67,
        "gender": "Male",
        "birthdate": datetime.date(1954, 12, 28),
    },
    {
        "name": "Cate Blanchett",
        "age": 52,
        "gender": "Female",
        "birthdate": datetime.date(1969, 5, 14),
    },
    {
        "name": "Leonardo DiCaprio",
        "age": 47,
        "gender": "Male",
        "birthdate": datetime.date(1974, 11, 11),
    },
]

MOVIES = [
    {"title": "The Masterpiece", "release_date": datetime.date(2020, 5, 15)},
    {"title": "Eternal Sunshine", "release_date": datetime.date(2019, 8, 22)},
    {"title": "Midnight in Paris", "release_date": datetime.date(2021, 2, 10)},
    {"title": "The Grand Adventure", "release_date": datetime.date(2018, 11, 5)},
    {"title": "Lost in Translation", "release_date": datetime.date(2022, 1, 20)},
]


def create_app_for_seeding():
    """Create a Flask app for seeding the database"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app


def seed_database():
    """Seed the database with sample data"""
    app = create_app_for_seeding()

    with app.app_context():
        # Clear existing data
        logger.info("Clearing existing data...")
        Movie.query.delete()
        Actor.query.delete()
        db.session.commit()

        # Create actors
        logger.info("Creating actors...")
        created_actors = []
        for actor_data in ACTORS:
            actor = Actor(**actor_data)
            with DBTransaction(message=f"Created actor: {actor.name}"):
                db.session.add(actor)
            created_actors.append(actor)

        # Create movies
        logger.info("Creating movies...")
        created_movies = []
        for movie_data in MOVIES:
            movie = Movie(**movie_data)
            with DBTransaction(message=f"Created movie: {movie.title}"):
                db.session.add(movie)
            created_movies.append(movie)

        # Assign actors to movies (each movie gets 2-4 random actors)
        logger.info("Assigning actors to movies...")
        for movie in created_movies:
            # Select 2-4 random actors for this movie
            num_actors = random.randint(2, 4)
            movie_actors = random.sample(created_actors, num_actors)

            with DBTransaction(message=f"Assigned actors to movie: {movie.title}"):
                for actor in movie_actors:
                    movie.actors.append(actor)
                    logger.info(f"Assigned {actor.name} to {movie.title}")

        logger.info("Database seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
