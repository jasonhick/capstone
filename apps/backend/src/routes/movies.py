from flask import Blueprint, abort, jsonify, request

from ..database import db
from ..models import Actor, Movie
from .error_handlers import register_error_handlers

movies_bp = Blueprint("movies", __name__)
register_error_handlers(movies_bp)


@movies_bp.route("/movies")
def get_movies():
    try:
        movies = Movie.query.all()
        return (
            jsonify(
                {"success": True, "movies": [movie.serialize() for movie in movies]}
            ),
            200,
        )
    except Exception as e:
        abort(500)


@movies_bp.route("/movies", methods=["POST"])
def create_movie():
    try:
        data = request.get_json()
        if not all(k in data for k in ("title", "release_date")):
            abort(400)

        new_movie = Movie(title=data["title"], release_date=data["release_date"])
        new_movie.insert()

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
    except Exception as e:
        abort(422)


@movies_bp.route("/movies/<int:movie_id>", methods=["PATCH"])
def update_movie(movie_id):
    try:
        movie = Movie.query.get_or_404(movie_id)
        data = request.get_json()

        if "title" in data:
            movie.title = data["title"]
        if "release_date" in data:
            movie.release_date = data["release_date"]

        movie.update()

        return (
            jsonify({"success": True, "updated": movie.id, "movie": movie.serialize()}),
            200,
        )
    except Exception as e:
        abort(422)


@movies_bp.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    try:
        movie = Movie.query.get_or_404(movie_id)
        movie.delete()

        return jsonify({"success": True, "deleted": movie_id}), 200
    except Exception as e:
        abort(422)


@movies_bp.route("/movies/<int:movie_id>/actors", methods=["GET"])
def get_movie_actors(movie_id):
    try:
        movie = Movie.query.get_or_404(movie_id)
        return (
            jsonify(
                {
                    "success": True,
                    "movie_id": movie_id,
                    "actors": [actor.serialize_brief() for actor in movie.actors],
                }
            ),
            200,
        )
    except Exception as e:
        abort(404)


@movies_bp.route("/movies/<int:movie_id>/actors", methods=["POST"])
def add_movie_actor(movie_id):
    try:
        movie = Movie.query.get_or_404(movie_id)
        data = request.get_json()

        if "actor_id" not in data:
            abort(400)

        actor = Actor.query.get_or_404(data["actor_id"])
        movie.actors.append(actor)
        movie.update()

        return (
            jsonify({"success": True, "movie_id": movie_id, "actor_id": actor.id}),
            201,
        )
    except Exception as e:
        abort(422)
