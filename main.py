import requests
import csv
import spacy
from service.request.get_profile import *
from service.request.get_financial import *
from service import Service
from ORMModels.company import *

# download = requests.get("https://raw.githubusercontent.com/justalak/data/master/data/VNX.csv")
# decoded_content = download.content.decode('utf-8')
# cr = csv.reader(decoded_content.splitlines(), delimiter=',')
# my_list = list(cr)
# for row in my_list[1:]:
#     # indicator = RequestFinancialIndicator.GetCompanyFinancialIndicator(row[0])
#     # indicator.save()
#     try:
#         reports = RequestFinancialReport.GetCompanyFinancialReport(row[0])
#         financial_report.FinancialReport.bulk_create(reports)
#         print("Fetched {symbol}".format(symbol=row[0]))
#     except:
#         print("Fetched {symbol} failed".format(symbol=row[0]))

file_path = Service.handle_business_report_action('HSG', 'quarter')
print(file_path)
