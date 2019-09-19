from marshmallow import Schema, fields, validate


class ToDoListSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, data_key="userId")
    name = fields.Str(required=True, validate=validate.Length(max=255))
    created = fields.DateTime(dump_only=True)
