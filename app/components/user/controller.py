from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError

import language as lang
from components.authtoken.model import AuthToken
from components.system.model import System
from helpers import api_message, json_required

from .model import User
from .schema import UserSchema

user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/user", methods=["POST"])
@json_required
def user():
    user_schema = UserSchema()

    # Validate Data
    try:
        data = user_schema.load(g.parsed_json)
    except (ValidationError) as e:
        return api_message(e.messages, 400)

    # Create and Return User
    password_salt = System.get("password_salt")
    user = User(data["email_address"], data["password"], password_salt)
    return jsonify(user_schema.dump(user)), 201


# TODO: Add DELETE method
@user_blueprint.route("/user/<int:user_id>", methods=["GET", "PATCH"])
@AuthToken.required
@json_required
def user_by_id(user_id):
    # If the user is trying to access data for another user return a 404
    if user_id != g.user_id:
        return api_message(lang.not_found, 404)

    user = User.get_by_id(g.user_id)
    if user is None:
        return api_message(lang.not_found, 404)

    # GET
    if request.method == "GET":
        return jsonify(UserSchema().dump(user))

    # PATCH
    elif request.method == "PATCH":
        # Validate Data
        try:
            data = UserSchema().load(g.parsed_json, partial=True)
        except ValidationError as e:
            return api_message(e.messages, 400)

        # Update and Return User
        user.update(data)
        return jsonify(UserSchema().dump(user))
