from datetime import datetime, timedelta
from functools import wraps
from uuid import uuid4

from flask import g, jsonify, request

from models.shared import db  # TODO

from .model import AuthToken


class AuthTokenService:
    @staticmethod
    def create(user_id):
        authtoken = AuthToken()

        authtoken.user_id = user_id

        now = datetime.now()
        authtoken.id = str(uuid4())
        authtoken.expiry = now + timedelta(days=30)
        authtoken.last_used = now
        authtoken.created = now

        db.session.add(authtoken)
        db.session.commit()

        return authtoken

    @staticmethod
    def get(token):
        return AuthToken.query.filter(
            AuthToken.id == token, AuthToken.expiry > datetime.now()
        ).first()

    @staticmethod
    def required(func):
        """Require an authentication token in order to execute the decorated
        function. Add the authenticated user to Flask's g local proxy.

        Args:
            func (function): The decorated function.

        Returns:
            If a valid token is passed the decorated function is returned,
            else a 401 response is returned.
        """

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            token_id = request.headers.get("token")
            if token_id is None:
                return (
                    jsonify({"message": "Authentication token missing."}),
                    401,
                )

            authtoken = AuthTokenService.get(token_id)
            if authtoken is None:
                return (
                    jsonify({"message": "Authentication token invalid."}),
                    401,
                )

            g.user_id = authtoken.user_id

            authtoken.last_used = datetime.now()
            db.session.commit()

            return func(*args, **kwargs)

        return wrapped_func

    @staticmethod
    def delete(authtoken, commit=True):
        db.session.delete(authtoken)
        if commit is True:
            db.session.commit()

        return authtoken.id

    @staticmethod
    def delete_expired():
        for authtoken in AuthToken.query.filter(
            AuthToken.expiry < datetime.now()
        ):
            AuthTokenService.delete(authtoken, commit=False)
        db.session.commit()
