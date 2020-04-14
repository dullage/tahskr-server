from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(max=64))
    password = fields.Str(
        load_only=True, required=True, validate=validate.Length(max=255)
    )
    config = fields.Dict()
    created = fields.DateTime(dump_only=True)
