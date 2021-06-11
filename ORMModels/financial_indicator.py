from peewee import *
from ORMModels import base, classification


class FinancialIndicator(base.BaseModel):
    id = AutoField()
    symbol = CharField(index=True, unique=False)
    PE = DecimalField()
    PS = DecimalField()
    PB = DecimalField()
    ROA = DecimalField()
    ROE = DecimalField()
    ROIC = DecimalField()
    ROCE = DecimalField()
    EPS = DecimalField()

    class Meta:
        table_name = "financial_indicator"

    @staticmethod
    def search_by_symbol(symbol):
        try:
            res = FinancialIndicator.get(FinancialIndicator.symbol == symbol)
            return res
        except:
            return None
