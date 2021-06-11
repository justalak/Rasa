from peewee import *
import json
from ORMModels import base, classification


class JSONField(Field):
    field_type = 'text'

    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        return json.loads(value)


class Request(base.BaseModel):
    id = AutoField()
    message = TextField()
    intent = CharField()
    sender_id = CharField()
    entities = JSONField()
    response_action = CharField()
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
