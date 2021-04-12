from service.common import date_range_type


def icb_code_to_classification(icb_code):
    return

def date_range_to_text(date_range):
    if date_range == date_range_type.MONTH_TYPE:
        return "theo tháng"
    elif date_range == date_range_type.SIX_MONTH_TYPE:
        return "6 tháng gần nhất"
    elif date_range == date_range_type.YEAR_TYPE:
        return "1 năm nay"
    else:
        return "3 tháng gần nhất"