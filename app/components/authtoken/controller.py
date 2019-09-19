from flask import Blueprint, g, jsonify
from marshmallow.exceptions import ValidationError

import language as lang
from helpers import api_message, json_required
from components.user import UserSchema, User

from .model import AuthToken
from .schema import AuthTokenSchema

authtoken_blueprint = Blueprint("authtoken", __name__)


@authtoken_blueprint.route("/auth", methods=["POST"])
@json_required
def auth():
    # Validate Data
    try:
        data = UserSchema().load(g.parsed_json)
    except ValidationError as e:
        return api_message(e.messages, 400)

    # Authenticate Credentials
    user = User.authenticate(data["email_address"], data["password"])
    if user is None:
        return api_message(lang.invalid_credentials, 401)

    # Create and Return AuthToken
    token = AuthToken(user.id)
    return jsonify(AuthTokenSchema().dump(token))
