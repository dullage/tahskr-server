from marshmallow import Schema, fields


class AuthTokenSchema(Schema):
    id = fields.Str(dump_only=True, data_key="token")
    user_id = fields.Int(required=True, data_key="userId")
    expiry = fields.DateTime(dump_only=True)
    last_used = fields.DateTime(dump_only=True, data_key="lastUsed")
    created = fields.DateTime(dump_only=True)
