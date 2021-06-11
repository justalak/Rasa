from peewee import *
from ORMModels import base, classification


class WatchStock(base.BaseModel):
    id = AutoField()
    sender_id = CharField(index=True)
    symbol = CharField(index=True)
