import requests
import csv
from service.request.get_profile import *
from service.request.get_financial import *
from ORMModels.company import *

download = requests.get("https://raw.githubusercontent.com/justalak/data/master/data/VNX.csv")
decoded_content = download.content.decode('utf-8')
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
my_list = list(cr)
for row in my_list[1:]:
    indicator = RequestFinancialIndicator.GetCompanyFinancialIndicator(row[0])
    indicator.save()

    reports = RequestFinancialReport.GetCompanyFinancialReport(row[0])
    financial_report.FinancialReport.bulk_create(reports)
