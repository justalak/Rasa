from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, events
from rasa_sdk.executor import CollectingDispatcher
import json
from ORMModels.company import *
from ORMModels.financial_indicator import *
from ORMModels.classification import *
from actions import hook
from service.data_process.extractor import *
from service import *


class ActionGetList(Action):

    def name(self) -> Text:
        return "action_get_branch_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        branches = Classification.select()
        text = ""
        for branch in branches:
            text += "👉 {branch_name}\n".format(branch_name=branch.name)

        dispatcher.utter_message(
            template="utter_answer_branch_list",
            branch_list=text
        )
        hook.after_processed(tracker, self.name())
        return []


class ActionGetFinance(Action):

    def name(self) -> Text:
        return "action_get_branch_finance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot("branch") is None:
            return [events.FollowupAction("action_get_branch_list")]

        branch_id = int(tracker.get_slot("branch"))
        branch = Classification.get_by_id(branch_id)
        number_of_companies = Company.count_by_branch(branch_id)
        top_profit_companies = Company.highest_profit_by_branch(branch_id)
        print(top_profit_companies)
        if branch.profit_growth > 10:
            comment = "khả quan"
        elif branch.profit_growth > 0:
            comment = "trung lập"
        else:
            comment = "kém khả quan"

        company_list = ""
        for company in top_profit_companies:
            company_list += "👉 {name} - mã *{symbol}*\n".format(name=company.name,
                                                                 symbol=company.symbol)
        dispatcher.utter_message(
            template="utter_answer_branch_finance",
            branch_name=branch.name,
            number_of_companies=number_of_companies,
            profit_growth=branch.profit_growth,
            pe_avg=branch.pe_avg,
            comment=comment
        )

        dispatcher.utter_message(
            template="utter_answer_top_profit",
            company_list=company_list,
            branch_name=branch.name
        )
        hook.after_processed(tracker, self.name())
        return []
