from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound, UnprocessableEntity

from ..common import get_logger
from ..common.error_handlers import APIError, handle_exception
from ..database import db
from ..models import Actor, Movie
from .error_handlers import register_error_handlers

movies_bp = Blueprint("movies", __name__)
register_error_handlers(movies_bp)

# Get logger
logger = get_logger()


@movies_bp.route("/movies")
@handle_exception
def get_movies():
    logger.info("Fetching all movies")
    movies = Movie.query.all()
    return jsonify([movie.serialize() for movie in movies]), 200


@movies_bp.route("/movies/<int:movie_id>", methods=["GET"])
@handle_exception
def get_movie(movie_id):
    logger.info(f"Fetching movie with ID: {movie_id}")
    movie = Movie.query.get_or_404(movie_id)
    return jsonify(movie.serialize()), 200


@movies_bp.route("/movies", methods=["POST"])
@handle_exception
def create_movie():
    data = request.get_json()
    logger.info(f"Creating new movie with data: {data}")

    if not all(k in data for k in ("title", "release_date")):
        logger.warning("Missing required fields in movie creation request")
        raise BadRequest("Missing required fields: title and release_date are required")

    new_movie = Movie(title=data["title"], release_date=data["release_date"])
    new_movie.insert()
    logger.info(f"Successfully created movie with ID: {new_movie.id}")

    return (
        jsonify(
            {
                "success": True,
                "created": new_movie.id,
                "movie": new_movie.serialize(),
            }
        ),
        201,
    )


@movies_bp.route("/movies/<int:movie_id>", methods=["PATCH"])
@handle_exception
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    data = request.get_json()
    logger.info(f"Updating movie with ID: {movie_id} with data: {data}")

    try:
        if "title" in data:
            movie.title = data["title"]
        if "release_date" in data:
            movie.release_date = data["release_date"]

        movie.update()
        logger.info(f"Successfully updated movie with ID: {movie_id}")

        return (
            jsonify({"success": True, "updated": movie_id, "movie": movie.serialize()}),
            200,
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating movie with ID {movie_id}: {str(e)}")
        raise UnprocessableEntity("Could not update movie")


@movies_bp.route("/movies/<int:movie_id>", methods=["DELETE"])
@handle_exception
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    logger.info(f"Deleting movie with ID: {movie_id}")

    try:
        movie.delete()
        logger.info(f"Successfully deleted movie with ID: {movie_id}")
        return jsonify({"success": True, "deleted": movie_id}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting movie with ID {movie_id}: {str(e)}")
        raise UnprocessableEntity("Could not delete movie")


@movies_bp.route("/movies/<int:movie_id>/actors", methods=["GET"])
@handle_exception
def get_movie_actors(movie_id):
    logger.info(f"Fetching actors for movie with ID: {movie_id}")
    movie = Movie.query.get_or_404(movie_id)
    return jsonify([actor.serialize_brief() for actor in movie.actors]), 200


@movies_bp.route("/movies/<int:movie_id>/actors", methods=["POST"])
@handle_exception
def add_movie_actor(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    data = request.get_json()
    logger.info(f"Adding actor to movie with ID: {movie_id}, data: {data}")

    if "actor_id" not in data:
        logger.warning(f"Missing actor_id in request to add actor to movie {movie_id}")
        raise BadRequest("Missing required field: actor_id")

    try:
        actor = Actor.query.get_or_404(data["actor_id"])
        movie.actors.append(actor)
        movie.update()
        logger.info(f"Successfully added actor {actor.id} to movie {movie_id}")

        return (
            jsonify({"success": True, "movie_id": movie_id, "actor_id": actor.id}),
            201,
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding actor to movie {movie_id}: {str(e)}")
        raise UnprocessableEntity("Could not add actor to movie")
