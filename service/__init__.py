from service.request import get_price, upload_image
import service.data_process as data_process
from service.common import date_range_type
import ORMModels.financial_report as financial_report
class Service:
    @staticmethod
    def HandleChangeCheatSeatAction(symbol, date_range):
        data = []
        if date_range == date_range_type.MONTH_TYPE:
            data = get_price.RequestPrice.PriceInMonth(symbol)
        elif date_range == date_range_type.SIX_MONTH_TYPE:
            data = get_price.RequestPrice.PriceInSixMonths(symbol)
        elif date_range == date_range_type.YEAR_TYPE:
            data = get_price.RequestPrice.PriceInYear(symbol)
        else:
            date_range = date_range_type.QUARTER_TYPE
            data = get_price.RequestPrice.PriceInQuarter(symbol)

        data = data[::-1]
        file_name = symbol + "_" + date_range + ".png"
        file_path = data_process.DataProcessor.exportToChartImage(data, file_name)
        file_url = upload_image.ImageUploader.Upload(file_path)
        return file_url

    @staticmethod
    def handle_business_report_action(symbol, time_range):
        if time_range is None:
            time_range = "quarter"
        sales = []
        net_profits = []
        times = []

        file_name = symbol + "_" + time_range + "_report" + ".png"
        reports = financial_report.FinancialReport.get_business_report(symbol, time_range)
        for report in reports:
            sales.append(report.sales/1000000000)
            net_profits.append(report.net_profit/1000000000)
            times.append(report.time)
        file_path = data_process.DataProcessor.exportToReportsChartImage(sales, net_profits, times, file_name)
        file_url = upload_image.ImageUploader.upload_sub(file_path)
        return file_url
