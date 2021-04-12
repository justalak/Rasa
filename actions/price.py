from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
from utils import time_format, display_text
from service.request.get_price import RequestPrice
from ORMModels.company import *
from service.common import constants, utils
import service


class ActionRequestPrice(Action):

    def name(self) -> Text:
        return "action_request_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        stock_code = tracker.get_slot("stock_code")
        if not stock_code:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_name'
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
            template='utter_support_after_answer_price',
            stock_code=stock_code
        )

        return []


class ActionRequestPriceCheatSheat(Action):

    def name(self) -> Text:
        return "action_request_price_change"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        stock_code = tracker.get_slot("stock_code")
        print(stock_code)
        date_range = tracker.get_slot("date_range")
        if not stock_code:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_code'
            )
            return []

        image_url = service.Service.HandleChangeCheatSeatAction(stock_code, date_range)
        date_range_text = utils.date_range_to_text(date_range=date_range)

        dispatcher.utter_message(
            template='utter_answer_price_change',
            chart_image=image_url,
            date_range_text=date_range_text
        )

        dispatcher.utter_message(
            template='utter_support_price_date_range'
        )

        return [SlotSet("stock_code", stock_code)]


class ActionRequestPriceByCompany(Action):

    def name(self) -> Text:
        return "action_request_price_by_company"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("company_name")
        result = Company.search_by_name(name)
        if len(result) == 0:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_name'
            )
            return []

        company = result[0]

        result = RequestPrice.CurrentPrice(company.symbol)
        date = result[0][constants.DATE]
        time = result[0][constants.TIME]

        dispatcher.utter_message(
            template='utter_answer_price_with_name',
            time=time_format.TimeHelper.toDisplayText(date, time),
            symbol=company.symbol,
            company_name=company.name,
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
            template='utter_support_after_answer_price',
            stock_code=company.symbol
        )

        return [SlotSet("stock_code", company.symbol)]
