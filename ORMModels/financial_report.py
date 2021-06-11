from peewee import *
from ORMModels import base, classification
from service.common import date_range_type

REPORT_YEAR_TYPE = 0
REPORT_QUARTER_TYPE = 1

class FinancialReport(base.BaseModel):
    id = AutoField()
    symbol = CharField(index=True, unique=False)
    type = IntegerField()
    time = CharField()
    sales = BigIntegerField()
    gross_profit = BigIntegerField()
    operating_profit = BigIntegerField()
    net_profit = BigIntegerField()

    class Meta:
        table_name = "financial_report"

    @staticmethod
    def get_last_report(symbol, time_range):
        try:
            if time_range == date_range_type.YEAR_TYPE:
                time = REPORT_YEAR_TYPE
            else:
                time = REPORT_QUARTER_TYPE
            res = FinancialReport.select().where(FinancialReport.symbol == symbol, FinancialReport.type == time)
            if len(res) == 0:
                return None
            else:
                return res[len(res) - 1]
        except:
            return None

    @staticmethod
    def get_business_report(symbol, time_range):
        if time_range == date_range_type.YEAR_TYPE:
            time = REPORT_YEAR_TYPE
        else:
            time = REPORT_QUARTER_TYPE
        res = FinancialReport.select().where(FinancialReport.symbol == symbol, FinancialReport.type == time)
        return res
