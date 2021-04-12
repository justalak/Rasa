import requests
from service.config import config
import base64
from service.common import constants

class ImageUploader:
    BaseUrl = "https://api.imgbb.com/1/upload"

    @staticmethod
    def Upload(filePath):
        with open(filePath, "rb") as file:
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": config.IMBB_API_KEY,
                "image": base64.b64encode(file.read()),
            }
            res = requests.post(url, payload)

        return res.json()['data']['image']['url']
