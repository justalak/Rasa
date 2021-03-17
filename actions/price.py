from typing import Any, Text, Dict, List
import csv
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from utils import time_format, display_text
from common.price import RequestPrice, constants

class ActionRequestPrice(Action):

    def name(self) -> Text:
        return "action_request_price"

    def code_string(self, code) -> Text:
        return "https://raw.githubusercontent.com/hoanglv-1009/data/master/data/VNX/{}/Price.csv".format(code)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        stock_code = tracker.get_slot("stock_code")
        if not stock_code:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_code'
            )
            return []

        result = RequestPrice.CurrentPrice(stock_code)
        date = result[0][constants.DATE]
        time = result[0][constants.TIME]


        dispatcher.utter_message(
            template='utter_answer_price',
            time=time_format.TimeHelper.toDisplayText(date, time),
            symbol=stock_code,
            basic_price=result[0][constants.PRICE_TYPE_BASIC],
            floor_price=result[0][constants.PRICE_TYPE_FLOOR],
            ceiling_price=result[0][constants.PRICE_TYPE_CEILING],
            high_price=result[0][constants.PRICE_TYPE_HIGH],
            low_price=result[0][constants.PRICE_TYPE_LOW],
            change=result[0][constants.PRICE_TYPE_AD_CHANGE],
            change_pct=result[0][constants.PRICE_TYPE_AD_CHANGE_PCT],
            change_symbol=display_text.DisplayHelper.numberToArrow(result[0][constants.PRICE_TYPE_AD_CHANGE])
        )

        dispatcher.utter_message(
            template='utter_more_info'
        )

        return []
