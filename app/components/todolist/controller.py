from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError

import language as lang
from components.authtoken.model import AuthToken
from components.todo.model import ToDo
from helpers import api_message, json_required

from .model import ToDoList
from .schema import ToDoListSchema

todolist_blueprint = Blueprint("todolist_blueprint", __name__)


@todolist_blueprint.route("/todolist", methods=["GET", "POST"])
@AuthToken.authenticate_user
@json_required
def todolist(auth_user_id):
    # GET
    if request.method == "GET":
        # Get and Return ToDoLists
        todolists = ToDoList.get_all_for_user(auth_user_id)
        return jsonify(
            [ToDoListSchema().dump(todolist) for todolist in todolists]
        )

    # POST
    elif request.method == "POST":
        # Validate Data
        try:
            data = ToDoListSchema(exclude=["user_id"]).load(g.parsed_json)
        except (ValidationError) as e:
            return api_message(e.messages, 400)

        # Create and Return ToDoList
        todolist = ToDoList(auth_user_id, data["name"])
        return jsonify(ToDoListSchema().dump(todolist)), 201


@todolist_blueprint.route(
    "/todolist/<int:todolist_id>", methods=["GET", "PATCH", "DELETE"]
)
@AuthToken.authenticate_user
@json_required
def todolist_by_id(todolist_id, auth_user_id):
    todolist = ToDoList.get_by_id_for_user(auth_user_id, todolist_id)
    if todolist is None:
        return api_message(lang.not_found, 404)

    # GET
    if request.method == "GET":
        return jsonify(ToDoListSchema().dump(todolist))

    # PATCH
    elif request.method == "PATCH":
        # Validate Data
        try:
            data = ToDoListSchema(exclude=["user_id"]).load(g.parsed_json)
        except ValidationError as e:
            return api_message(e.messages, 400)

        # Update and Return ToDoList
        todolist.update(data)
        return jsonify(ToDoListSchema().dump(todolist))

    # DELETE
    elif request.method == "DELETE":
        for todo in ToDo.get_by_list_id(todolist.id):
            todo.update({"list_id": None}, commit=False)
        todolist.delete(commit=True)
        return api_message(lang.deletion_successful, 200)
