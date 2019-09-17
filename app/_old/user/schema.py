from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email_address = fields.Email(required=True, data_key="emailAddress")
    password = fields.Str(required=True)
    created = fields.DateTime(dump_only=True)
