from models.shared import db  # TODO


class AuthToken(db.Model):
    __tablename__ = "AuthToken"

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    last_used = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
