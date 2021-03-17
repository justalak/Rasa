
from datetime import datetime

class TimeHelper:
    @staticmethod
    def toDisplayText(date_string, time_string):
        time = datetime.strptime(date_string+" "+time_string, '%Y-%m-%d %H:%M:%S')
        return time.strftime("%H giờ %M phút ngày %d/%m/%Y")