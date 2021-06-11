from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from actions import mapping
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, FollowupAction
from utils import time_format, display_text
from service.request.get_price import RequestPrice
from ORMModels.company import *
from rasa_sdk import Action, Tracker, events
from service.data_process import extractor
from service.common import constants, utils
import service
import json


class UnsetStockCode(Action):
    def name(self) -> Text:
        return "action_unset_stock_code"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Unset stock code")
        tracker.slots['stock_code'] = None
        intent = tracker.latest_message['intent'].get('name')
        print(intent)
        return []

class ActionExtractName(Action):

    def name(self) -> Text:
        return "action_extract_company_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        company_name = extractor.Extractor.extract_company_name(tracker.latest_message.get("text"))
        res = Company.search_by_name(company_name)

        if len(res) == 0:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_name'
            )
            return []

        company = res[0]
        print(company)
        stock_code = company.symbol
        if len(res) > 1:
            company_list = []
            for result in res:
                item = {
                    "name": result.name,
                    "symbol": result.symbol,
                }
                company_list.append(item)

            dispatcher.utter_message(

            )
            dispatcher.utter_message(
                template="utter_support_other_search_result",
                company_name=company.name,
                stock_code=stock_code
            )
            return [events.SlotSet("stock_code", stock_code),
                    events.SlotSet("result_list", json.dumps(company_list)),
                    events.SlotSet("current_intent", tracker.latest_message['intent'].get('name')),
                   ]

        intent = tracker.latest_message['intent'].get('name')
        next_action = mapping.intent_action_map[intent]

        return [events.SlotSet("stock_code", stock_code),
                events.SlotSet("current_intent", intent),
                events.FollowupAction(next_action)]


class SetIntent(Action):
    def name(self) -> Text:
        return "action_set_intent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        print(intent)
        tracker.slots['current_intent'] = intent
        return []


class ProcessRequest(Action):
    def name(self) -> Text:
        return "action_continue_request"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_intent = tracker.get_slot("current_intent")
        print(current_intent)
        next_intent = mapping.intent_action_map[current_intent]
        return [FollowupAction(next_intent)]


