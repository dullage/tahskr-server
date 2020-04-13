import os
import secrets

from flask import Flask

from components.authtoken.controller import authtoken_blueprint
from components.system.model import System
from components.todo.controller import todo_blueprint
from components.todolist.controller import todolist_blueprint
from components.user.controller import user_blueprint
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///database.db"
)

db.init_app(app)
with app.app_context():
    # Initialise Database
    db.create_all()
    db.session.commit()

    # Initialise Password Salt
    password_salt_key = "password_salt"
    if System.get(password_salt_key) is None:
        System({"key": password_salt_key, "value": secrets.token_urlsafe(32)})

app.register_blueprint(user_blueprint)
app.register_blueprint(authtoken_blueprint)
app.register_blueprint(todolist_blueprint)
app.register_blueprint(todo_blueprint)
