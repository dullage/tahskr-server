import os

from flask import Flask

from components.authtoken import authtoken_blueprint
from components.todo import todo_blueprint
from components.todolist import todolist_blueprint
from components.user import user_blueprint
from shared import db

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///database.db"
)

db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

app.register_blueprint(user_blueprint)
app.register_blueprint(authtoken_blueprint)
app.register_blueprint(todolist_blueprint)
app.register_blueprint(todo_blueprint)
