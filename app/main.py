import os

from flask import Flask

from authtoken import token_blueprint
from todo import todo_blueprint
from todolist import todolist_blueprint
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///database.db"
)

db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

app.register_blueprint(token_blueprint)
app.register_blueprint(todo_blueprint)
app.register_blueprint(todolist_blueprint)
