from datetime import date, datetime

from helpers import setattrs
from models.shared import db  # TODO

from .model import ToDo


class ToDoService:
    @staticmethod
    def create(user_id, attrs):
        todo = ToDo()
        todo.user_id = user_id
        todo = setattrs(todo, attrs)
        todo.created = datetime.now()

        db.session.add(todo)
        db.session.commit()

        return todo

    @staticmethod
    def get_by_id(user_id, todo_id):
        return ToDo.query.filter_by(user_id=user_id, id=todo_id).first()

    @staticmethod
    def get_all(
        user_id, parent_id=None, completed=None, exclude_snoozed=False
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
        query = ToDo.query.filter_by(user_id=user_id, parent_id=parent_id)
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

    @staticmethod
    def update(todo, attrs):
        todo = setattrs(todo, attrs)
        db.session.commit()
        return todo

    @staticmethod
    def delete(todo, commit=True):
        for subtask in ToDo.query.filter_by(parent_id=todo.id).all():
            ToDoService.delete(subtask, commit=False)
        db.session.delete(todo)

        if commit is True:
            db.session.commit()

        return todo.id
