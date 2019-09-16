from models.shared import db  # TODO


class ToDo(db.Model):
    __tablename__ = "ToDo"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    summary = db.Column(db.String, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("ToDo.id"))
    list_id = db.Column(db.Integer, db.ForeignKey("ToDoList.id"))
    notes = db.Column(db.Text)
    completed_datetime = db.Column(db.DateTime)
    # rank = db.Column(db.Integer, nullable=False)  # TODO: Unique constraint?
    starred = db.Column(db.Boolean, nullable=False)
    snooze_date = db.Column(db.Date)
    created = db.Column(db.DateTime, nullable=False)
