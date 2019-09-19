from flask import Blueprint, g, jsonify
from marshmallow import ValidationError

from helpers import api_message, json_required

from .model import User
from .schema import UserSchema

user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/api/user", methods=["POST"])
@json_required
def user():
    user_schema = UserSchema()

    # Validate Data
    try:
        data = user_schema.load(g.parsed_json)
    except (ValidationError) as e:
        return api_message(e.messages, 400)

    # Create and Return ToDo
    user = User(data["email_address"], data["password"])
    return jsonify(user_schema.dump(user)), 201
