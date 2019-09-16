from flask import Blueprint, g, jsonify, request
from marshmallow import Schema, ValidationError, fields

import language as lang
from authtoken import AuthTokenService
from helpers import api_message, json_required

from .schema import ToDoSchema
from .service import ToDoService

todo_blueprint = Blueprint("todo_blueprint", __name__)


@todo_blueprint.route("/api/todo", methods=["GET", "POST"])
@AuthTokenService.required
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
        todos = ToDoService.get_all(
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
        todo = ToDoService.create(g.user_id, data)
        return jsonify(ToDoSchema().dump(todo)), 201


@todo_blueprint.route(
    "/api/todo/<int:todo_id>", methods=["GET", "PATCH", "DELETE"]
)
@AuthTokenService.required
@json_required
def todo_by_id(todo_id):
    todo = ToDoService.get_by_id(g.user_id, todo_id)
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
        todo = ToDoService.update(todo, data)
        return jsonify(ToDoSchema().dump(todo))

    # DELETE
    elif request.method == "DELETE":
        return api_message(ToDoService.delete(todo), 200)
