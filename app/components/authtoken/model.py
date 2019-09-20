from datetime import datetime, timedelta
from functools import wraps
from uuid import uuid4

from flask import g, jsonify, request

from components.base import Base
from shared import db


class AuthToken(db.Model, Base):
    __tablename__ = "AuthToken"

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    last_used = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id

        now = datetime.now()
        self.id = str(uuid4())
        self.expiry = now + timedelta(days=30)
        self.last_used = now
        self.created = now

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_active_by_id(cls, token):
        return cls.query.filter(
            cls.id == token, cls.expiry > datetime.now()
        ).first()

    @classmethod
    def required(cls, func):
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
            token = request.headers.get("token")
            if token is None:
                return (
                    jsonify({"message": "Authentication token missing."}),
                    401,
                )

            authtoken = cls.get_active_by_id(token)
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

    # def delete(self, commit=True):
    #     db.session.delete(self)
    #     if commit is True:
    #         db.session.commit()
    #     return self.id

    @classmethod
    def delete_expired(cls):
        for authtoken in cls.query.filter(cls.expiry < datetime.now()):
            authtoken.delete(commit=False)
        db.session.commit()
