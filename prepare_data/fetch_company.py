import requests
import csv
from service.request.get_profile import *
from ORMModels.company import *

download = requests.get("https://raw.githubusercontent.com/justalak/data/master/data/VNX.csv")
decoded_content = download.content.decode('utf-8')
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
my_list = list(cr)
for row in my_list[1:]:
    res = RequestProfile.GetCompanyProfile(row[0])
    res.save()
