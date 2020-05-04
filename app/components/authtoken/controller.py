from flask import Blueprint, g, jsonify
from marshmallow.exceptions import ValidationError

import language as lang
from components.system.model import System
from components.user.model import User
from components.user.schema import UserSchema
from helpers import api_message, json_required

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
    password_salt = System.get("password_salt").value
    user = User.authenticate(data["username"], data["password"], password_salt)
    if user is None:
        return api_message(lang.credentials_invalid, 401)

    # Data Cleanse
    AuthToken.delete_expired()

    # Create and Return AuthToken
    token = AuthToken(user.id)
    return jsonify(AuthTokenSchema().dump(token))
