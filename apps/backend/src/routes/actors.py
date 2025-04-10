from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound, UnprocessableEntity

from ..auth.auth import (
    DELETE_ACTORS,
    GET_ACTORS,
    PATCH_ACTORS,
    POST_ACTORS,
    requires_auth,
)
from ..common import get_logger
from ..common.error_handlers import APIError, handle_exception, register_error_handlers
from ..database import DBTransaction, db
from ..models import Actor

actors_bp = Blueprint("actors", __name__)
register_error_handlers(actors_bp)

# Get logger
logger = get_logger()


@actors_bp.route("/actors")
@requires_auth(GET_ACTORS)
@handle_exception
def get_actors(payload):
    logger.info("Fetching all actors")
    actors = Actor.get_all()
    return jsonify([actor.serialize() for actor in actors]), 200


@actors_bp.route("/actors/<int:actor_id>", methods=["GET"])
@requires_auth(GET_ACTORS)
@handle_exception
def get_actor(payload, actor_id):
    logger.info(f"Fetching actor with ID: {actor_id}")
    actor = Actor.get_or_404(actor_id)
    return jsonify(actor.serialize()), 200


@actors_bp.route("/actors", methods=["POST"])
@requires_auth(POST_ACTORS)
@handle_exception
def create_actor(payload):
    data = request.get_json()
    logger.info(f"Creating new actor with data: {data}")

    if not all(k in data for k in ("name", "age", "gender")):
        logger.warning("Missing required fields in actor creation request")
        raise BadRequest("Missing required fields: name, age, and gender are required")

    new_actor = Actor(name=data["name"], age=data["age"], gender=data["gender"])

    if "birthdate" in data and data["birthdate"]:
        new_actor.birthdate = data["birthdate"]

    new_actor.insert()
    logger.info(f"Successfully created actor with ID: {new_actor.id}")

    return (
        jsonify(
            {
                "success": True,
                "created": new_actor.id,
                "actor": new_actor.serialize(),
            }
        ),
        201,
    )


@actors_bp.route("/actors/<int:actor_id>", methods=["PATCH"])
@requires_auth(PATCH_ACTORS)
@handle_exception
def update_actor(payload, actor_id):
    actor = Actor.get_or_404(actor_id)
    data = request.get_json()
    logger.info(f"Updating actor with ID: {actor_id} with data: {data}")

    try:
        if "name" in data:
            actor.name = data["name"]
        if "age" in data:
            actor.age = data["age"]
        if "gender" in data:
            actor.gender = data["gender"]
        if "birthdate" in data:
            actor.birthdate = data["birthdate"]

        with DBTransaction(message=f"Updated actor with ID: {actor_id}"):
            pass  # The transaction will commit automatically

        return (
            jsonify(
                {
                    "success": True,
                    "updated": actor.id,
                    "actor": actor.serialize_brief(),
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Error updating actor with ID {actor_id}: {str(e)}")
        raise UnprocessableEntity("Could not update actor")


@actors_bp.route("/actors/<int:actor_id>", methods=["DELETE"])
@requires_auth(DELETE_ACTORS)
@handle_exception
def delete_actor(payload, actor_id):
    actor = Actor.get_or_404(actor_id)
    logger.info(f"Deleting actor with ID: {actor_id}")

    try:
        with DBTransaction(message=f"Deleted actor with ID: {actor_id}"):
            db.session.delete(actor)

        return jsonify({"success": True, "deleted": actor_id}), 200
    except Exception as e:
        logger.error(f"Error deleting actor with ID {actor_id}: {str(e)}")
        raise UnprocessableEntity("Could not delete actor")
