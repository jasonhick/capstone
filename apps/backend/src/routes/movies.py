from flask import Blueprint, abort, jsonify, request

from ..database import db
from ..models import Movie
from .error_handlers import register_error_handlers

movies_bp = Blueprint("movies", __name__)
register_error_handlers(movies_bp)


@movies_bp.route("/movies")
def get_movies():
    try:
        movies = Movie.query.all()
        return (
            jsonify(
                {
                    "success": True,
                    "movies": [
                        {
                            "id": movie.id,
                            "title": movie.title,
                            "release_date": movie.release_date.isoformat(),
                        }
                        for movie in movies
                    ],
                }
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
        db.session.add(new_movie)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "created": new_movie.id,
                    "movie": {
                        "id": new_movie.id,
                        "title": new_movie.title,
                        "release_date": new_movie.release_date.isoformat(),
                    },
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
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

        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "updated": movie.id,
                    "movie": {
                        "id": movie.id,
                        "title": movie.title,
                        "release_date": movie.release_date.isoformat(),
                    },
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        abort(422)


@movies_bp.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    try:
        movie = Movie.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()

        return jsonify({"success": True, "deleted": movie_id}), 200
    except Exception as e:
        db.session.rollback()
        abort(422)
