# %% Import libraries
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime
from urllib import request

class Helpers:
    @staticmethod
    def loadJson(symbol, rtype, quarter=0, count=10):
        url_path = 'https://svr1.fireant.vn/api/Data/Finance/LastestFinancialReports?symbol={}&type={}&year={}&quarter={}&count={}'.format(
            symbol, rtype, datetime.now().year, quarter, count)

        with request.urlopen(url_path) as url:
            jdata = json.loads(url.read().decode())
            if jdata is None:
                return None

            data = None
            for col in jdata:
                if data is None:
                    data = pd.DataFrame(col['Values']).rename(columns={'Value': col['Name']}).set_index(
                        ['Year', 'Quarter'])
                else:
                    data[col['Name']] = pd.DataFrame(col['Values']).set_index(['Year', 'Quarter']).Value

            if data is None:
                return None

            return data

        return None

    @staticmethod
    def BalanceSheetQuarter(symbol):
        """Get balance sheet quarterly

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadJson(symbol, 1, 4, 40)

    @staticmethod
    def IncomeStatementQuarter(symbol):
        """Get imcome statement quarterly

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadJson(symbol, 2, 4, 40)

    @staticmethod
    def DCashFlowQuarter(symbol):
        """Get direct cash flow quarterly

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadJson(symbol, 3, 4, 40)

    @staticmethod
    def ICashFlowQuarter(symbol):
        """Get indirect cash flow quarterly

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadJson(symbol, 4, 4, 40)

    @staticmethod
    def CashFlowQuarter(symbol):
        """Get cash flow quarterly

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        cfq = Fundamentals.ICashFlowQuarter(symbol)
        if cfq is None:
            return Fundamentals.DCashFlowQuarter(symbol)

        return cfq

    @staticmethod
    def BalanceSheet(symbol):
        """Get balance sheet data

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadJson(symbol, 1)

    @staticmethod
    def IncomeStatement(symbol):
        """Get income statement data

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadJson(symbol, 2)

    @staticmethod
    def DCashFlow(symbol):
        """Get direct cash flow data

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadJson(symbol, 3)

    @staticmethod
    def ICashFlow(symbol):
        """Get indirect cash flow data

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadJson(symbol, 4)

    @staticmethod
    def CashFlow(symbol):
        """Get cash flow data

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        cf = Fundamentals.ICashFlow(symbol)
        if cf is None:
            return Fundamentals.DCashFlow(symbol)

        return cf