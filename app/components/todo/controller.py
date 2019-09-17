from flask import Blueprint, g, jsonify, request
from marshmallow import Schema, ValidationError, fields

import language as lang
from components.authtoken import AuthToken
from helpers import api_message, json_required

from .model import ToDo
from .schema import ToDoSchema

todo_blueprint = Blueprint("todo_blueprint", __name__)


@todo_blueprint.route("/api/todo", methods=["GET", "POST"])
@AuthToken.required
@json_required
def todo():
    # GET
    if request.method == "GET":
        # Validate Data
        arg_schema = Schema.from_dict(
            {
                "parent_id": fields.Int(missing=None, data_key="parentId"),
                "completed": fields.Bool(missing=None),
                "exclude_snoozed": fields.Bool(missing=False),
            }
        )

        data = request.args.to_dict()
        try:
            data = arg_schema().load(data)
        except ValidationError as e:
            return api_message(e.messages, 400)

        # Get and Return ToDos
        todos = ToDo.get_multiple_for_user(
            g.user_id,
            parent_id=data["parent_id"],
            completed=data["completed"],
            exclude_snoozed=data["exclude_snoozed"],
        )

        return jsonify([ToDoSchema().dump(todo) for todo in todos])

    # POST
    elif request.method == "POST":
        # Validate Data
        try:
            data = ToDoSchema(exclude=["user_id"]).load(g.parsed_json)
        except (ValidationError) as e:
            return api_message(e.messages, 400)

        # TODO: Validate the parent and list ids exist for the user.

        # Create and Return ToDo
        todo = ToDo(g.user_id, data)
        return jsonify(ToDoSchema().dump(todo)), 201


@todo_blueprint.route(
    "/api/todo/<int:todo_id>", methods=["GET", "PATCH", "DELETE"]
)
@AuthToken.required
@json_required
def todo_by_id(todo_id):
    todo = ToDo.get_by_id_for_user(g.user_id, todo_id)
    if todo is None:
        return api_message(lang.not_found, 404)

    # GET
    if request.method == "GET":
        return jsonify(ToDoSchema().dump(todo))

    # PATCH
    elif request.method == "PATCH":
        # Validate Data
        try:
            data = ToDoSchema(exclude=["user_id"]).load(
                g.parsed_json, partial=True
            )
        except ValidationError as e:
            return api_message(e.messages, 400)

        # TODO: Validate the parent and list ids exist for the user.

        # Update and Return ToDo
        todo.update(data)
        return jsonify(ToDoSchema().dump(todo))

    # DELETE
    elif request.method == "DELETE":
        for subtask in ToDo.get_by_parent_id(todo.id):
            subtask.delete(commit=False)
        todo.delete(commit=True)
        return api_message("Deletion successful", 200)
