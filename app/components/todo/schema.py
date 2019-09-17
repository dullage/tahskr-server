from marshmallow import Schema, fields


class ToDoSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, data_key="userId")
    summary = fields.Str(required=True)
    parent_id = fields.Int(allow_none=True, missing=None, data_key="parentId")
    list_id = fields.Int(allow_none=True, missing=None, data_key="listId")
    notes = fields.Str(allow_none=True, missing=None)
    completed_datetime = fields.DateTime(
        allow_none=True, missing=None, data_key="completedDatetime"
    )
    starred = fields.Bool(missing=False)
    snooze_date = fields.Date(
        allow_none=True, missing=None, data_key="snoozeDate"
    )
    created = fields.DateTime(dump_only=True)

    # TODO: Character lengths.
