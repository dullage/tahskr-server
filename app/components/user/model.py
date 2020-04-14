from datetime import datetime

from components.base.model import Base
from helpers import hash_password
from db import db


class User(db.Model, Base):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    failed_login_attempts = db.Column(db.Integer, nullable=False)
    locked = db.Column(db.Boolean, nullable=False)
    config = db.Column(db.PickleType)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, password, password_salt):
        self.username = username.lower()
        self.password = hash_password(password, password_salt)
        self.failed_login_attempts = 0
        self.locked = False
        self.created = datetime.utcnow()

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username.lower()).first()

    @classmethod
    def authenticate(cls, username, password, password_salt):
        """TODO

        Args:
            username (str)
            password (str)

        Returns:
            User
        """
        user = cls.get_by_username(username)

        if user is None:
            return None
        if user.locked is True:
            return (
                None
            )  # TODO: Let the API consumer know and allow them to reset.
        if hash_password(password, password_salt) != user.password:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.locked = True
            db.session.commit()
            return None
        else:
            user.failed_login_attempts = 0
            db.session.commit()
            return user
