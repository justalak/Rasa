# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import csv
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionRequestPrice(Action):

    def name(self) -> Text:
        return "action_request_price"

    def code_string(self, code) -> Text:
        return "https://raw.githubusercontent.com/hoanglv-1009/data/master/data/VNX/{}/Price.csv".format(code)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_code = tracker.get_slot("stock_code")
        print(stock_code)
        download = requests.get(self.code_string(stock_code))
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        last_updated = my_list.pop()
        # print(my_list)

        text = "Cổ phiếu mã  {} cập nhật vào {} có giá là : \nOpen: {}\nHigh: {}\nLow: {}".format(
            tracker.get_slot("stock_code"), last_updated[0], last_updated[1], last_updated[2], last_updated[3])

        dispatcher.utter_message(text=text)

        return []

class ActionRequestAssets(Action):

    def name(self) -> Text:
        return "action_request_assets"

    def code_string(self, code) -> Text:
        return "https://raw.githubusercontent.com/hoanglv-1009/data/master/data/VNX/{}/BalanceSheetQuarter.csv".format(code)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_code = tracker.get_slot("stock_code")
        print(stock_code)
        download = requests.get(self.code_string(stock_code))
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        last_updated = my_list.pop()
        # print(my_list)

        text = "Tài sản ngắn hạn của {} cập nhật vào quý {} năm {} có giá là : {}".format(
            tracker.get_slot("stock_code"), last_updated[1], last_updated[0], last_updated[2])

        dispatcher.utter_message(text=text)

        return []

class ActionRequestSale(Action):

    def name(self) -> Text:
        return "action_request_sale"

    def code_string(self, code) -> Text:
        return "https://raw.githubusercontent.com/hoanglv-1009/data/master/data/VNX/{}/IncomeStatementQuarter.csv".format(code)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_code = tracker.get_slot("stock_code")
        print(stock_code)
        download = requests.get(self.code_string(stock_code))
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        last_updated = my_list.pop()
        # print(my_list)

        text = "doanh thu của của {} cập nhật vào quý {} năm {}: \nTổng doanh thu:  {} \nCác khoản giảm trừ: {}\nDoanh thu thuần: {}".format(
            tracker.get_slot("stock_code"), last_updated[1], last_updated[0], last_updated[2], last_updated[3], last_updated[4])

        dispatcher.utter_message(text=text)

        return []
