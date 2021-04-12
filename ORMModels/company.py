from peewee import *
from ORMModels import base, classification

MIN_SCORE = 5

class Company(base.BaseModel):
    id = AutoField()
    name = CharField()
    short_name = CharField()
    date_of_issue = DateTimeField()
    date_of_listing = DateTimeField()
    employees = IntegerField()
    symbol = CharField(index=True, unique=True)
    listing_volume = IntegerField()
    icb_code = CharField()
    classification = ForeignKeyField(classification.Classification)
    overview = TextField()

    @staticmethod
    def search_by_name(query):
        res = Company.select().where(SQL("MATCH(name, short_name, symbol) AGAINST('{query}') > {min_score}"
                                         .format(query=query, min_score=MIN_SCORE)))
        return res

    @staticmethod
    def search_by_symbol(symbol):
        try:
            res = Company.get(Company.symbol == symbol)
            return res
        except:
            return None
