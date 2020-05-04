from marshmallow import Schema, fields, validate


class SystemSchema(Schema):
    key = fields.Str(required=True, validate=validate.Length(max=255))
    value = fields.Str(required=True, validate=validate.Length(max=255))
