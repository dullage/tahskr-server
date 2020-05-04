import os

from flask import Flask, jsonify

import database
from components.authtoken.controller import authtoken_blueprint
from components.system.model import System
from components.todo.controller import todo_blueprint
from components.todolist.controller import todolist_blueprint
from components.user.controller import user_blueprint
from db import db
from helpers import get_version, init_database_url

APP_DIR_PATH = os.path.dirname(__file__)

__version__ = get_version(APP_DIR_PATH)

database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    database_url = init_database_url(APP_DIR_PATH)

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_url

database.init(db, app)


@app.route("/")
def index():
    return jsonify(
        {
            "appVersion": __version__,
            "schemaVersion": System.get("schema_version").value,
        }
    )


app.register_blueprint(user_blueprint)
app.register_blueprint(authtoken_blueprint)
app.register_blueprint(todolist_blueprint)
app.register_blueprint(todo_blueprint)
