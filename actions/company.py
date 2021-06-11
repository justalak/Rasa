from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, events
from rasa_sdk.executor import CollectingDispatcher
import json
from ORMModels.company import *
from ORMModels.financial_indicator import *
from ORMModels.financial_report import *
from actions import hook
from service.data_process.extractor import *
from service import *


class ActionGetInfo(Action):

    def name(self) -> Text:
        return "action_get_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
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
                symbol=company.symbol,
                company_name=company.name,
                overview=company.overview,
                classification=company.classification.name,
                employees=company.employees,
                listing_volume='{:,}'.format(company.listing_volume),
                date_of_issue=company.date_of_issue.strftime("%d/%m/%Y")
            )

            hook.after_processed(tracker, "action_get_info")
            return []
        except:
            hook.after_processed(tracker, "action_get_info")
            dispatcher.utter_message("Có lỗi xảy ra 😔 Hãy thử lại sau!")
            return []


class ShowSearchResult(Action):

    def name(self) -> Text:
        return "action_show_search_result"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            result_list = json.loads(tracker.get_slot("result_list"))
            result_text = []
            for company in result_list:
                result_text.append("👉 *{name}* - mã *{symbol}*".format(name=company["name"],
                                                                        symbol=company["symbol"]))

            dispatcher.utter_message(
                template="utter_list_results",
                result_text="\n".join(result_text)
            )
            dispatcher.utter_message(
                template="utter_ask_exact_code",
            )

            hook.after_processed(tracker, "action_show_search_result")
            return [events.SlotSet("stock_code", None)]
        except:
            hook.after_processed(tracker, "action_get_info")
            dispatcher.utter_message("Có lỗi xảy ra 😔 Hãy thử lại sau!")
            return []


class ActionGetFinancialIndicator(Action):
    def name(self) -> Text:
        return "action_get_financial_indicator"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            stock_code = tracker.get_slot("stock_code")
            if not stock_code:
                dispatcher.utter_message(
                    template='utter_ask_particular_stock_name'
                )
                return []

            res = FinancialIndicator.search_by_symbol(symbol=stock_code)
            company = Company.search_by_symbol(symbol=stock_code)
            if not res:
                dispatcher.utter_message(
                    template='utter_ask_particular_stock_name'
                )
                return []

            dispatcher.utter_message(
                template='utter_answer_company_financial',
                company_name=company.name,
                pe='{:.2f}'.format(res.PE),
                ps='{:.2f}'.format(res.PS),
                eps='{:.2f}'.format(res.EPS),
                pb='{:.2f}'.format(res.PB),
                roa='{:.2f}%'.format(res.ROA),
                roe='{:.2f}%'.format(res.ROE),
                roic='{:.2f}%'.format(res.ROIC),
                roce='{:.2f}%'.format(res.ROCE),
            )

            hook.after_processed(tracker, "action_get_financial_indicator")
            return []
        except:
            hook.after_processed(tracker, "action_get_financial_indicator")
            dispatcher.utter_message("Có lỗi xảy ra 😔 Hãy thử lại sau!")
            return []


class ActionGetBusinessResult(Action):
    def name(self) -> Text:
        return "action_get_business_result"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        stock_code = tracker.get_slot("stock_code")
        date_range = tracker.get_slot("date_range")

        if not stock_code:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_name'
            )
            return []

        if date_range == "year":
            time = "năm"
        else:
            time = "quý"
        res = FinancialReport.get_last_report(symbol=stock_code, time_range=date_range)
        company = Company.search_by_symbol(symbol=stock_code)
        dispatcher.utter_message(
            template='utter_answer_business_result',
            company_name=company.name,
            time=res.time,
            sales='{:.2f}'.format(res.sales/1000000000),
            gross_profit='{:.2f}'.format(res.gross_profit/1000000000),
            operating_profit='{:.2f}'.format(res.operating_profit/1000000000),
            net_profit='{:.2f}'.format(res.net_profit/1000000000),
        )

        dispatcher.utter_message(
            template="utter_refer_business_report",
            symbol=stock_code,
            date_range=time
        )

        hook.after_processed(tracker, "action_get_business_result")
        return [events.SlotSet("stock_code", stock_code)]

class ActionEvaluateBusiness(Action):
    def name(self) -> Text:
        return "action_evaluate_business"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        stock_code = tracker.get_slot("stock_code")
        date_range = tracker.get_slot("date_range")

        print(stock_code)
        if not stock_code:
            dispatcher.utter_message(
                template='utter_ask_particular_stock_name'
            )
            return []

        image_url = Service.handle_business_report_action(stock_code, date_range)
        company = Company.search_by_symbol(symbol=stock_code)
        dispatcher.utter_message(
            template='utter_answer_business_set_report',
            company_name=company.name,
            image_url=image_url
        )

        hook.after_processed(tracker, "action_evaluate_business")
        return []
