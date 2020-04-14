from helpers import setattrs
from db import db


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
    def get(cls, key):
        return cls.query.get(key)
