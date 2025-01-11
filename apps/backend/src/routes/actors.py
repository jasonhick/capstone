from flask import Blueprint, jsonify, request

from ..database import db
from ..models import Actor

actors_bp = Blueprint("actors", __name__)


@actors_bp.route("/actors")
def get_actors():
    actors = Actor.query.all()
    return jsonify(
        [
            {
                "id": actor.id,
                "name": actor.name,
                "age": actor.age,
                "gender": actor.gender,
            }
            for actor in actors
        ]
    )


@actors_bp.route("/actors", methods=["POST"])
def create_actor():
    data = request.get_json()
    new_actor = Actor(name=data["name"], age=data["age"], gender=data["gender"])
    db.session.add(new_actor)
    db.session.commit()
    return jsonify({"id": new_actor.id}), 201


@actors_bp.route("/actors/<int:actor_id>", methods=["PATCH"])
def update_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    data = request.get_json()

    if "name" in data:
        actor.name = data["name"]
    if "age" in data:
        actor.age = data["age"]
    if "gender" in data:
        actor.gender = data["gender"]

    db.session.commit()
    return jsonify({"success": True})


@actors_bp.route("/actors/<int:actor_id>", methods=["DELETE"])
def delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    db.session.delete(actor)
    db.session.commit()
    return jsonify({"success": True})
