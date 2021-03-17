import spacy
from _datetime import datetime
import csv
import requests
import yaml
from common import price
from utils import time_format

url = "https://raw.githubusercontent.com/justalak/data/master/data/VNX.csv"
download = requests.get(url)
decoded_content = download.content.decode('utf-8')
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
result_list = list(cr)

time_str = "22:11:10"
date_str = "2021-03-15"

print(time_format.TimeHelper.toDisplayText(date_str, time_str))