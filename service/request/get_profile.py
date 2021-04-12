import requests
from service.common import constants
from datetime import datetime
from ORMModels import company

BASE_URL = "https://restv2.fireant.vn/symbols/{code}/profile"


class RequestProfile:
    @staticmethod
    def GetCompanyProfile(symbol):
        base_url = BASE_URL.format(code=symbol)
        res = requests.get(base_url, headers={'Authorization': constants.TOKEN})
        data = res.json()
        return company.Company(
            name=data['companyName'],
            short_name=data['shortName'],
            date_of_issue=datetime.strptime(data['dateOfIssue'], '%Y-%m-%dT%H:%M:%S'),
            date_of_listing=datetime.strptime(data['dateOfIssue'], '%Y-%m-%dT%H:%M:%S'),
            employees=data['employees'],
            symbol=symbol,
            listing_volume=data['listingVolume'],
            icb_code=data['icbCode'],
            overview=data['overview'],
            classification_id=RequestProfile.icb_code_to_classification(int(data['icbCode']))
        )

    @staticmethod
    def icb_code_to_classification(icb_code):
        if icb_code < 1300:
            return 1
        elif icb_code < 1700:
            return 2
        elif icb_code < 2300:
            return 3
        elif icb_code < 2700:
            return 4
        elif icb_code < 3300:
            return 5
        elif icb_code < 3500:
            return 6
        elif icb_code < 3700:
            return 7
        elif icb_code < 4500:
            return 8
        elif icb_code < 5300:
            return 9
        elif icb_code < 5500:
            return 10
        elif icb_code < 5700:
            return 12
        elif icb_code < 6000:
            return 11
        elif icb_code < 7000:
            return 13
        elif icb_code < 8300:
            return 14
        elif icb_code < 8500:
            return 15
        elif icb_code < 8600:
            return 16
        elif icb_code < 8700:
            return 17
        elif icb_code < 9000:
            return 18
        else:
            return 19
