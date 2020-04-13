import os

from flask import Flask

import database
from components.authtoken.controller import authtoken_blueprint
from components.todo.controller import todo_blueprint
from components.todolist.controller import todolist_blueprint
from components.user.controller import user_blueprint
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///database.db"
)

database.init(db, app)

app.register_blueprint(user_blueprint)
app.register_blueprint(authtoken_blueprint)
app.register_blueprint(todolist_blueprint)
app.register_blueprint(todo_blueprint)
