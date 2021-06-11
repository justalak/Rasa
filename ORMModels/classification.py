from peewee import *
from ORMModels import base


class Classification(base.BaseModel):
    id = AutoField()
    code = CharField()
    name = CharField(max_length=255)
    profit_growth = FloatField()
    pe_avg = FloatField()
