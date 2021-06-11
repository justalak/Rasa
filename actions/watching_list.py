from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from actions import mapping
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, FollowupAction
from utils import time_format, display_text
from service.request.get_price import RequestPrice
from ORMModels.watch_stock import *
from service.common import constants, utils
import service
from actions import hook


class AddToWatchingList(Action):
    def name(self) -> Text:
        return "action_add_to_watching_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        stock_code = tracker.get_slot("stock_code")
        if stock_code is None:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_name'
            )
            return []
        sender_id = tracker.current_state()['sender_id']
        if sender_id is None:
            sender_id = "rasa-shell"

        res = WatchStock.select().where(WatchStock.sender_id == sender_id and WatchStock.symbol == stock_code)
        if len(res) > 0:
            dispatcher.utter_message(
                template="utter_add_to_watch_list_fail",
                stock_code=stock_code
            )
        else:
            WatchStock.create(symbol=stock_code, sender_id=sender_id)
            dispatcher.utter_message(
                template="utter_add_to_watch_list_success",
                stock_code=stock_code
            )

        dispatcher.utter_message(
            template="utter_ask_for_show_list",
        )

        hook.after_processed(tracker, "action_add_to_watching_list")

        return []


class RemoveFromWatchingList(Action):
    def name(self) -> Text:
        return "action_remove_from_watching_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        stock_code = tracker.get_slot("stock_code")
        if stock_code is None:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_name'
            )
            return []
        sender_id = tracker.current_state()['sender_id']
        if sender_id is None:
            sender_id = "rasa-shell"

        res = WatchStock.select().where(WatchStock.sender_id == sender_id and WatchStock.symbol == stock_code)
        if len(res) == 0:
            dispatcher.utter_message(
                template="utter_remove_from_watch_list_fail",
                stock_code="stock_code"
            )
        else:
            q = WatchStock.get(symbol=stock_code, sender_id=sender_id)
            q.delete_instance()
            dispatcher.utter_message(
                template="utter_remove_from_watch_list_success",
                stock_code=stock_code
            )
        dispatcher.utter_message(
            template="utter_ask_for_show_list",
        )

        hook.after_processed(tracker, "action_remove_from_watching_list")
        return []


class ShowWatchingList(Action):
    def name(self) -> Text:
        return "action_show_watching_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender_id = tracker.current_state()['sender_id']
        if sender_id is None:
            sender_id = "rasa-shell"

        res = WatchStock.select().where(WatchStock.sender_id == sender_id)
        if len(res) == 0:
            dispatcher.utter_message(
                template="utter_inform_empty_list",
            )
            return []

        for item in res:
            result = RequestPrice.CurrentPrice(item.symbol)
            date = result[0][constants.DATE]
            time = result[0][constants.TIME]

            dispatcher.utter_message(
                template='utter_answer_price',
                time=time_format.TimeHelper.toDisplayText(date, time),
                symbol=item.symbol,
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
            template="utter_more_info"
        )
        hook.after_processed(tracker, "action_show_watching_list")
        return []
