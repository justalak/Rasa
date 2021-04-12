from service.common import constants
from service.config import config
import mplfinance as fplt
import pandas as pd


class DataProcessor:
    @staticmethod
    def exportToDataFrame(jsonData):
        reformatted_data = dict()
        reformatted_data['Date'] = []
        reformatted_data['Open'] = []
        reformatted_data['High'] = []
        reformatted_data['Low'] = []
        reformatted_data['Close'] = []
        reformatted_data['Volume'] = []

        for unit in jsonData:
            reformatted_data['Date'].append(pd.to_datetime(unit[constants.DATE]))
            reformatted_data['Open'].append(unit[constants.PRICE_TYPE_OPEN])
            reformatted_data['High'].append(unit[constants.PRICE_TYPE_HIGH])
            reformatted_data['Low'].append(unit[constants.PRICE_TYPE_LOW])
            reformatted_data['Close'].append(unit[constants.PRICE_TYPE_CLOSE])
            reformatted_data['Volume'].append(unit[constants.PRICE_TYPE_VOLUME])

        df = pd.DataFrame.from_dict(reformatted_data)
        df.set_index('Date', inplace=True)
        return df

    @staticmethod
    def exportToChartImage(json_data, file_name):
        data_frame = DataProcessor.exportToDataFrame(json_data)
        file_path = config.IMAGES_DIRECTORY + file_name
        fplt.plot(
            data_frame,
            type='candle',
            style='charles',
            show_nontrading=False,
            # title='Apple, March - 2020',
            ylabel='Mức giá',
            figratio=(12, 6),
            volume=True,
            ylabel_lower='Số lương',
            savefig=file_path
        )
        return file_path


