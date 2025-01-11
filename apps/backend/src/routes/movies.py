from flask import Blueprint, jsonify, request

from ..database import db
from ..models import Movie

movies_bp = Blueprint("movies", __name__)


@movies_bp.route("/movies")
def get_movies():
    movies = Movie.query.all()
    return jsonify(
        [
            {
                "id": movie.id,
                "title": movie.title,
                "release_date": movie.release_date.isoformat(),
            }
            for movie in movies
        ]
    )


@movies_bp.route("/movies", methods=["POST"])
def create_movie():
    data = request.get_json()
    new_movie = Movie(title=data["title"], release_date=data["release_date"])
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({"id": new_movie.id}), 201


@movies_bp.route("/movies/<int:movie_id>", methods=["PATCH"])
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    data = request.get_json()

    if "title" in data:
        movie.title = data["title"]
    if "release_date" in data:
        movie.release_date = data["release_date"]

    db.session.commit()
    return jsonify({"success": True})


@movies_bp.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"success": True})
