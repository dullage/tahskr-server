from models.shared import db  # TODO


class ToDoList(db.Model):
    __tablename__ = "ToDoList"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
