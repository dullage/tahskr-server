from datetime import datetime

from helpers import hash_password
from models.shared import PASSWORD_SALT, db
from todo import ToDoService
from todolist import ToDoListService
from authtoken import AuthTokenService, AuthToken

from .model import User


class UserService:
    @staticmethod
    def create(email_address, password):
        user = User()

        user.email_address = email_address.lower()
        user.password = hash_password(password, PASSWORD_SALT)
        user.failed_login_attempts = 0
        user.locked = False
        user.created = datetime.now()

        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def authenticate(email_address, password):
        """TODO

        Args:
            email_address (str)
            password (str)

        Returns:
            User
        """
        user = User.query.filter_by(
            email_address=email_address.lower()
        ).first()

        if user is None:
            return None
        if user.locked is True:
            return None  # TODO
        if hash_password(password, PASSWORD_SALT) != user.password:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 3:
                user.locked = True
            db.session.commit()
            return None
        else:
            return user

    @staticmethod
    def delete_by_id(user_id):
        user = UserService.get_by_id(user_id)

        for authtoken in AuthToken.query.filter_by(user_id=user_id):
            AuthTokenService.delete(authtoken, commit=False)

        for todo in ToDoService.get_all(user_id):
            ToDoService.delete(todo, commit=False)

        for todolist in ToDoListService.get_all(user_id):
            ToDoListService.delete(todolist, commit=False)

        db.session.delete(user)
        db.session.commit()
