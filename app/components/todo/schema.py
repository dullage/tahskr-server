from marshmallow import Schema, fields, validate


class ToDoSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, load_only=True, data_key="userId")
    summary = fields.Str(required=True, validate=validate.Length(max=255))
    parent_id = fields.Int(allow_none=True, missing=None, data_key="parentId")
    list_id = fields.Int(allow_none=True, missing=None, data_key="listId")
    notes = fields.Str(allow_none=True, missing=None)
    completed_datetime = fields.DateTime(
        allow_none=True, missing=None, data_key="completedDatetime"
    )
    important = fields.Bool(missing=False)
    snooze_date = fields.Date(
        allow_none=True, missing=None, data_key="snoozeDate"
    )
    rank = fields.Decimal(allow_none=True, missing=None)
    created = fields.DateTime(dump_only=True)
