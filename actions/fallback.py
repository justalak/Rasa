from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from actions import mapping, hook
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


class FallbackAction(Action):
    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        hook.after_fallback(tracker)
        dispatcher.utter_message(
            template="utter_fallback_response"
        )

        return []
