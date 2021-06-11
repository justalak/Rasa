import requests
from service.common import constants
from datetime import datetime
from ORMModels import company, financial_indicator, financial_report

INDICATOR_URL = "https://restv2.fireant.vn/symbols/{code}/financial-indicators"
REPORT_URL = "https://restv2.fireant.vn/symbols/{code}/financial-reports?type=IS&period={period}&compact=true&offset=0&limit=5"


class RequestFinancialIndicator:
    @staticmethod
    def GetCompanyFinancialIndicator(symbol):
        indicator_url = INDICATOR_URL.format(code=symbol)
        res = requests.get(indicator_url, headers={'Authorization': constants.TOKEN})
        data = res.json()
        return financial_indicator.FinancialIndicator(
            symbol=symbol,
            PE=data[0]['value'],
            PS=data[1]['value'],
            PB=data[2]['value'],
            EPS=data[3]['value'],
            ROA=data[12]['value'],
            ROE=data[13]['value'],
            ROIC=data[14]['value'],
            ROCE=data[15]['value']
        )


class RequestFinancialReport:
    @staticmethod
    def GetCompanyFinancialReport(symbol):
        report_url = REPORT_URL.format(code=symbol, period='Y')
        res = requests.get(report_url, headers={'Authorization': constants.TOKEN})
        data = res.json()
        result_list = []
        for i in range(2, 7):
            result_list.append(financial_report.FinancialReport(
                symbol=symbol,
                type=financial_report.REPORT_YEAR_TYPE,
                time=data['columns'][i],
                sales=data['rows'][0][i],
                gross_profit=data['rows'][1][i],
                operating_profit=data['rows'][2][i],
                net_profit=data['rows'][3][i]
            ))

        report_url = REPORT_URL.format(code=symbol, period='Q')
        res = requests.get(report_url, headers={'Authorization': constants.TOKEN})
        data = res.json()
        for i in range(2, 7):
            result_list.append(financial_report.FinancialReport(
                symbol=symbol,
                type=financial_report.REPORT_QUARTER_TYPE,
                time=data['columns'][i],
                sales=data['rows'][0][i],
                gross_profit=data['rows'][1][i],
                operating_profit=data['rows'][2][i],
                net_profit=data['rows'][3][i]
            ))

        return result_list
