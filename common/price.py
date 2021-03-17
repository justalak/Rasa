# %% Import libraries
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import requests
from common import constants

class RequestPrice:
    @staticmethod
    def loadJson(symbol, start_date, end_date):
        query = 'code:' + symbol + '~date:gte:' + start_date + '~date:lte:' + end_date
        delta = datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
        params = {
            "sort": "date",
            "size": delta.days + 1,
            "page": 1,
            "q": query
        }
        res = requests.get(constants.API_VNDIRECT, params=params)
        data = res.json()['data']
        return data

    @staticmethod
    def PriceInPeriodOfDays(symbol, days):
        current_date = datetime.today()
        begin_date = current_date - timedelta(days=days)
        return RequestPrice.loadJson(symbol, begin_date.strftime("%Y-%m-%d"), current_date.strftime("%Y-%m-%d"))

    @staticmethod
    def CurrentPrice(symbol):
        current_date = datetime.today()
        if current_date.isoweekday() == 6:
            last_friday = current_date - timedelta(days=1)
            return RequestPrice.loadJson(symbol, last_friday.strftime("%Y-%m-%d"), last_friday.strftime("%Y-%m-%d"))
        elif current_date.isoweekday() == 7:
            last_friday = current_date - timedelta(days=2)
            return RequestPrice.loadJson(symbol, last_friday.strftime("%Y-%m-%d"), last_friday.strftime("%Y-%m-%d"))
        else:
            return RequestPrice.loadJson(symbol, current_date.strftime("%Y-%m-%d"), current_date.strftime("%Y-%m-%d"))

    @staticmethod
    def PriceInMonth(symbol):
        return RequestPrice.PriceInPeriodOfDays(symbol, 30)

    @staticmethod
    def PriceInQuarter(symbol):
        return RequestPrice.loadJson(symbol, 30 * 4)

    @staticmethod
    def PriceInSixMonths(symbol):
        return RequestPrice.loadJson(symbol, 30 * 6)

    @staticmethod
    def PriceInSixYear(symbol):
        return RequestPrice.loadJson(symbol, 365)
    #
    # @staticmethod
    # def ICashFlowQuarter(symbol):
    #     """Get indirect cash flow quarterly
    #
    #     Keyword arguments:
    #     symbol (str) -- Asset symbol
    #     """
    #     return Fundamentals.loadJson(symbol, 4, 4, 40)
    #
    # @staticmethod
    # def CashFlowQuarter(symbol):
    #     """Get cash flow quarterly
    #
    #     Keyword arguments:
    #     symbol (str) -- Asset symbol
    #     """
    #     cfq = Fundamentals.ICashFlowQuarter(symbol)
    #     if cfq is None:
    #         return Fundamentals.DCashFlowQuarter(symbol)
    #
    #     return cfq
    #
    # @staticmethod
    # def BalanceSheet(symbol):
    #     """Get balance sheet data
    #
    #     Keyword arguments:
    #     symbol (str) -- Asset symbol
    #     """
    #     return Fundamentals.loadJson(symbol, 1)
    #
    # @staticmethod
    # def IncomeStatement(symbol):
    #     """Get income statement data
    #
    #     Keyword arguments:
    #     symbol (str) -- Asset symbol
    #     """
    #     return Fundamentals.loadJson(symbol, 2)
    #
    # @staticmethod
    # def DCashFlow(symbol):
    #     """Get direct cash flow data
    #
    #     Keyword arguments:
    #     symbol (str) -- Asset symbol
    #     """
    #     return Fundamentals.loadJson(symbol, 3)
    #
    # @staticmethod
    # def ICashFlow(symbol):
    #     """Get indirect cash flow data
    #
    #     Keyword arguments:
    #     symbol (str) -- Asset symbol
    #     """
    #     return Fundamentals.loadJson(symbol, 4)
    #
    # @staticmethod
    # def CashFlow(symbol):
    #     """Get cash flow data
    #
    #     Keyword arguments:
    #     symbol (str) -- Asset symbol
    #     """
    #     cf = Fundamentals.ICashFlow(symbol)
    #     if cf is None:
    #         return Fundamentals.DCashFlow(symbol)
    #
    #     return cf
