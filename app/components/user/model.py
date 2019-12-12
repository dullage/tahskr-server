from datetime import datetime

from components.base.model import Base
from helpers import hash_password
from shared import PASSWORD_SALT, db


class User(db.Model, Base):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    failed_login_attempts = db.Column(db.Integer, nullable=False)
    locked = db.Column(db.Boolean, nullable=False)
    config = db.Column(db.PickleType)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, email_address, password):
        self.email_address = email_address.lower()
        self.password = hash_password(password, PASSWORD_SALT)
        self.failed_login_attempts = 0
        self.locked = False
        self.created = datetime.utcnow()

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_email_address(cls, email_address):
        return cls.query.filter_by(email_address=email_address.lower()).first()

    @classmethod
    def authenticate(cls, email_address, password):
        """TODO

        Args:
            email_address (str)
            password (str)

        Returns:
            User
        """
        user = cls.get_by_email_address(email_address)

        if user is None:
            return None
        if user.locked is True:
            return (
                None
            )  # TODO: Let the API consumer know and allow them to reset.
        if hash_password(password, PASSWORD_SALT) != user.password:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 3:
                user.locked = True
            db.session.commit()
            return None
        else:
            return user
