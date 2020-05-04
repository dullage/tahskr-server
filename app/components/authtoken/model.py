from datetime import datetime, timedelta
from functools import wraps
from uuid import uuid4

from flask import request

import language as lang
from components.base.model import Base
from db import db
from helpers import api_message, check_admin_password


class AuthToken(db.Model, Base):
    __tablename__ = "AuthToken"

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    last_used = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id

        now = datetime.utcnow()
        self.id = str(uuid4())
        self.expiry = now + timedelta(days=30)
        self.last_used = now
        self.created = now

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_active_by_id(cls, token):
        return cls.query.filter(
            cls.id == token, cls.expiry > datetime.utcnow()
        ).first()

    @classmethod
    def authenticate_user_or_admin(cls, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            decl_admin_password = request.headers.get("x-admin")
            decl_token = request.headers.get("x-token")

            if decl_admin_password is None and decl_token is None:
                return api_message(lang.auth_token_missing, 401)

            # Authenticate Admin
            if decl_admin_password is not None:
                if check_admin_password(decl_admin_password) is False:
                    return api_message(lang.admin_password_invalid, 401)

                kwargs["auth_user_id"] = 0

            # Authenticate User
            else:
                authtoken = cls.get_active_by_id(decl_token)
                if authtoken is None:
                    return api_message(lang.auth_token_invalid, 401)

                kwargs["auth_user_id"] = authtoken.user_id

                authtoken.last_used = datetime.utcnow()
                db.session.commit()

            return func(*args, **kwargs)

        return wrapped_func

    @classmethod
    def authenticate_user(cls, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            decl_token = request.headers.get("x-token")
            if decl_token is None:
                return api_message(lang.auth_token_missing, 401)

            authtoken = cls.get_active_by_id(decl_token)
            if authtoken is None:
                return api_message(lang.auth_token_invalid, 401)

            kwargs["auth_user_id"] = authtoken.user_id

            authtoken.last_used = datetime.utcnow()
            db.session.commit()

            return func(*args, **kwargs)

        return wrapped_func

    @classmethod
    def authenticate_admin(cls, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            decl_admin_password = request.headers.get("x-admin")
            if decl_admin_password is None:
                return api_message(lang.admin_password_missing, 401)

            if check_admin_password(decl_admin_password) is False:
                return api_message(lang.admin_password_invalid, 401)

            return func(*args, **kwargs)

        return wrapped_func

    @classmethod
    def delete_expired(cls):
        for authtoken in cls.query.filter(cls.expiry < datetime.utcnow()):
            authtoken.delete(commit=False)
        db.session.commit()
