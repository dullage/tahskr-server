from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError

import language as lang
from authtoken import AuthToken
from helpers import api_message, json_required

from .schema import ToDoListSchema
from .service import ToDoListService

todolist_blueprint = Blueprint("todolist_blueprint", __name__)


@todolist_blueprint.route("/api/todolist", methods=["GET", "POST"])
@AuthToken.required
@json_required
def todolist():
    # GET
    if request.method == "GET":
        # Get and Return ToDoLists
        todolists = ToDoListService.get_all(g.user_id)
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
        todolist = ToDoListService.create(g.user_id, data["name"])
        return jsonify(ToDoListSchema().dump(todolist)), 201


@todolist_blueprint.route(
    "/api/todolist/<int:todolist_id>", methods=["GET", "PATCH", "DELETE"]
)
@AuthToken.required
@json_required
def todolist_by_id(todolist_id):
    todolist = ToDoListService.get_by_id(g.user_id, todolist_id)
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
        todolist = ToDoListService.update(todolist, data["name"])
        return jsonify(ToDoListSchema().dump(todolist))

    # DELETE
    elif request.method == "DELETE":
        return api_message(ToDoListService.delete(todolist), 200)
