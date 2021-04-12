from service.request import get_price, upload_image
import service.data_process as data_process
from service.common import date_range_type


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
