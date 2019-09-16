from datetime import datetime

from models.shared import db  # TODO
from todo import ToDo

from .model import ToDoList


class ToDoListService:
    @staticmethod
    def create(user_id, name):
        todolist = ToDoList()

        todolist.user_id = user_id
        todolist.name = name
        todolist.created = datetime.now()

        db.session.add(todolist)
        db.session.commit()

        return todolist

    @staticmethod
    def get_by_id(user_id, todolist_id):
        return ToDoList.query.filter_by(
            user_id=user_id, id=todolist_id
        ).first()

    @staticmethod
    def get_all(user_id):
        return ToDoList.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update(todolist, name):
        todolist.name = name
        db.session.commit()
        return todolist

    @staticmethod
    def delete(todolist, commit=True):
        for todo in ToDo.query.filter_by(list_id=todolist.id).all():
            todo.list_id = None
        db.session.delete(todolist)

        if commit is True:
            db.session.commit()

        return todolist.id
