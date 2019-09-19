from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email_address = fields.Email(
        required=True,
        validate=validate.Length(max=64),
        data_key="emailAddress",
    )
    password = fields.Str(
        load_only=True, required=True, validate=validate.Length(max=255)
    )
    created = fields.DateTime(dump_only=True)
