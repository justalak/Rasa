from peewee import *
from ORMModels import base, classification, financial_report

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

    @staticmethod
    def count_by_branch(branch_id):
        res = Company.select().join(classification.Classification) \
            .where(classification.Classification.id == branch_id)
        return len(res)

    @staticmethod
    def highest_profit_by_branch(branch_id):
        res = Company.select().join(classification.Classification) \
            .join(financial_report.FinancialReport, on=(Company.symbol == financial_report.FinancialReport.symbol)) \
            .where(financial_report.FinancialReport.type == financial_report.REPORT_YEAR_TYPE,
                   financial_report.FinancialReport.time == "2020",
                   classification.Classification.id == branch_id) \
            .order_by(financial_report.FinancialReport.net_profit.desc()) \
            .limit(3)
        return res
