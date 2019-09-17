from marshmallow import Schema, fields


class ToDoListSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, data_key="userId")
    name = fields.Str(required=True)
    created = fields.DateTime(dump_only=True)
