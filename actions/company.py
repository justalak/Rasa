from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, events
from rasa_sdk.executor import CollectingDispatcher
import json
from ORMModels.company import *
from service.data_process.extractor import *


class ActionGetInfo(Action):

    def name(self) -> Text:
        return "action_get_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        stock_code = tracker.get_slot("stock_code")
        if not stock_code:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_name'
            )
            return []

        res = Company.search_by_symbol(symbol=stock_code)
        if not res:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_name'
            )
            return []

        company = res
        dispatcher.utter_message(
            template='utter_answer_company_overview',
            company_name=company.name,
            overview=company.overview
        )

        dispatcher.utter_message(
            template='utter_answer_company_basic_info',
            classification=company.classification.name,
            employees=company.employees,
            listing_volume='{:,}'.format(company.listing_volume),
            date_of_issue=company.date_of_issue.strftime("%d/%m/%Y")
        )

        return []


class ActionExtractName(Action):

    def name(self) -> Text:
        return "action_extract_company_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        company_name = Extractor.extract_company_name(tracker.latest_message.get("text"))
        res = Company.search_by_name(company_name)
        print(res)
        if len(res) == 0:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_name'
            )
            return []

        company = res[0]
        stock_code = company.symbol
        # company_list = json.dumps([ob.__dict__ for ob in res])

        return [events.SlotSet("stock_code", stock_code), events.FollowupAction("action_get_info")]
