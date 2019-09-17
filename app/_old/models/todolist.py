from models.shared import db


class ToDoList(db.Model):
    __tablename__ = "List"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False)
