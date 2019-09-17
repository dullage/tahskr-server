from datetime import date, datetime

from helpers import datetime_to_str
from models.shared import db


class ToDo(db.Model):
    __tablename__ = "ToDo"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("ToDo.id"))
    list_id = db.Column(db.Integer, db.ForeignKey("List.id"))
    summary = db.Column(db.String, nullable=False)
    notes = db.Column(db.Text)
    completed_datetime = db.Column(db.DateTime)
    rank = db.Column(db.Integer, nullable=False)  # TODO: Unique constraint
    starred = db.Column(db.Boolean, nullable=False)
    snooze_date = db.Column(db.Date)
    created_datetime = db.Column(db.DateTime, nullable=False)

    def __init__(
        self, user_id, summary, notes=None, parent_id=None, list_id=None
    ):
        self.user_id = user_id
        self.summary = summary
        self.notes = notes
        self.parent_id = parent_id
        self.list_id = list_id

        self.rank = 0  # TODO
        self.starred = False
        self.created_datetime = datetime.now()

    def get_data(self):
        """Return a json.dumps compatible dictionary of ToDo data.

        Returns:
            dict
        """
        return {
            "id": self.id,
            "list_id": self.list_id,
            "summary": self.summary,
            "notes": self.notes,
            "completed_datetime": datetime_to_str(self.completed_datetime),
            "rank": self.rank,
            "starred": self.starred,
            "snooze_date": datetime_to_str(self.snooze_date),
            "created_datetime": datetime_to_str(self.created_datetime),
        }

    @classmethod
    def get(cls, user_id, todo_id):
        """Return an individual todo for a user by id.

        Args:
            user_id (int)
            todo_id (int)

        Returns:
            ToDo
        """
        return cls.query.filter_by(user_id=user_id, id=todo_id).first()

    @classmethod
    def get_multiple(
        cls, user_id, parent_id=None, completed=None, exclude_snoozed=False
    ):
        """Return a list of ToDo's based on the declared filters.

        Args:
            user_id (int): Only return ToDo's for this user.

            parent_id (int, optional): Only return ToDo's that are subtasks of
            this ToDo. Defaults to None.

            completed (bool, optional): True = Return only completed,
            False = Return only incomplete. Defaults to None (either).

            exclude_snoozed (bool, optional): Exclude those with a snooze_date
            after today. Defaults to False.

        Returns:
            [type]: [description]
        """
        query = cls.query.filter_by(user_id=user_id, parent_id=parent_id)
        if completed is False:
            query = query.filter_by(completed_datetime=None)
        if completed is True:
            query = query.filter(ToDo.completed_datetime.isnot(None))
        if exclude_snoozed is True:
            query = query.filter(
                (ToDo.snooze_date <= date.today())
                | (ToDo.snooze_date.is_(None))
            )

        return query.all()
