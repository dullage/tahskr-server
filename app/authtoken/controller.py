from flask import Blueprint, jsonify, g
from marshmallow.exceptions import ValidationError

import language as lang
from helpers import api_message, json_required
from user import UserSchema, UserService

from .schema import AuthTokenSchema
from .service import AuthTokenService

token_blueprint = Blueprint("token", __name__)


@token_blueprint.route("/auth", methods=["POST"])
@json_required
def auth():
    # Validate Data
    try:
        data = UserSchema().load(g.parsed_json)
    except ValidationError as e:
        return api_message(e.messages, 400)

    # Authenticate Credentials
    user = UserService.authenticate(data["email_address"], data["password"])
    if user is None:
        return api_message(lang.invalid_credentials, 401)

    # Create and Return AuthToken
    token = AuthTokenService.create(user.id)
    return jsonify(AuthTokenSchema().dump(token))
