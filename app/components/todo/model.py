from datetime import datetime

from components.base.model import Base
from helpers import setattrs
from shared import db


class ToDo(db.Model, Base):
    __tablename__ = "ToDo"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("ToDo.id"))
    list_id = db.Column(db.Integer, db.ForeignKey("ToDoList.id"))
    notes = db.Column(db.Text)
    completed_datetime = db.Column(db.DateTime)
    important = db.Column(db.Boolean, nullable=False)
    snooze_date = db.Column(db.Date)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, attrs):
        self.user_id = user_id
        setattrs(self, attrs)

        self.created = datetime.utcnow()

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_multiple_for_user(
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
            List of ToDo
        """
        query = cls.query.filter_by(user_id=user_id, parent_id=parent_id)
        if completed is False:
            query = query.filter_by(completed_datetime=None)
        if completed is True:
            query = query.filter(ToDo.completed_datetime.isnot(None))
        if exclude_snoozed is True:
            query = query.filter(
                (cls.snooze_date <= datetime.utcnow().date)
                | (cls.snooze_date.is_(None))
            )
        # TODO: Do the above date comparison based on a user supplied date to
        # account for TZ differences.

        return query.all()

    @classmethod
    def get_by_parent_id(cls, parent_id):
        return cls.query.filter_by(parent_id=parent_id).all()

    @classmethod
    def get_by_list_id(cls, list_id):
        return cls.query.filter_by(list_id=list_id).all()
