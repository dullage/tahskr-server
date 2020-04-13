import secrets

from helpers import setattrs
from shared import db


class System(db.Model):
    __tablename__ = "System"

    key = db.Column(db.String(255), primary_key=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)

    def __init__(self, attrs):
        setattrs(self, attrs)
        db.session.add(self)
        db.session.commit()

    def update(self, attrs, commit=True):
        setattrs(self, attrs)
        if commit is True:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        if commit is True:
            db.session.commit()
        return self.id

    @classmethod
    def get_by_key(cls, key):
        return cls.query.get(key)

    @classmethod
    def get_password_salt(cls):
        key = "password_salt"
        password_salt = cls.get_by_key(key)
        if password_salt is None:
            password_salt = cls(
                {"key": key, "value": secrets.token_urlsafe(32)}
            )
        return password_salt.value
