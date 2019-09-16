from models.shared import db


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    failed_login_attempts = db.Column(db.Integer, nullable=False)
    locked = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
