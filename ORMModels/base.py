from peewee import *
from ORMModels import Database


class BaseModel(Model):
    class Meta:
        database = Database.getDB()
