from flask import Blueprint, abort, jsonify, request

from ..database import db
from ..models import Actor
from .error_handlers import register_error_handlers

actors_bp = Blueprint("actors", __name__)
register_error_handlers(actors_bp)


@actors_bp.route("/actors")
def get_actors():
    try:
        actors = Actor.query.all()
        return (
            jsonify(
                {
                    "success": True,
                    "actors": [
                        {
                            "id": actor.id,
                            "name": actor.name,
                            "age": actor.age,
                            "gender": actor.gender,
                        }
                        for actor in actors
                    ],
                }
            ),
            200,
        )
    except Exception as e:
        abort(500)


@actors_bp.route("/actors", methods=["POST"])
def create_actor():
    try:
        data = request.get_json()
        if not all(k in data for k in ("name", "age", "gender")):
            abort(400)

        new_actor = Actor(name=data["name"], age=data["age"], gender=data["gender"])
        db.session.add(new_actor)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "created": new_actor.id,
                    "actor": {
                        "id": new_actor.id,
                        "name": new_actor.name,
                        "age": new_actor.age,
                        "gender": new_actor.gender,
                    },
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        abort(422)


@actors_bp.route("/actors/<int:actor_id>", methods=["PATCH"])
def update_actor(actor_id):
    try:
        actor = Actor.query.get_or_404(actor_id)
        data = request.get_json()

        if "name" in data:
            actor.name = data["name"]
        if "age" in data:
            actor.age = data["age"]
        if "gender" in data:
            actor.gender = data["gender"]

        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "updated": actor.id,
                    "actor": {
                        "id": actor.id,
                        "name": actor.name,
                        "age": actor.age,
                        "gender": actor.gender,
                    },
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        abort(422)


@actors_bp.route("/actors/<int:actor_id>", methods=["DELETE"])
def delete_actor(actor_id):
    try:
        actor = Actor.query.get_or_404(actor_id)
        db.session.delete(actor)
        db.session.commit()

        return jsonify({"success": True, "deleted": actor_id}), 200
    except Exception as e:
        db.session.rollback()
        abort(422)
