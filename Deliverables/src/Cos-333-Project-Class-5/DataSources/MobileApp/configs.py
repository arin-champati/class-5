""" @citation Adapted from: 
https://github.com/vr2amesh/COS333-API-Code-Examples/blob/master/MobileApp/python/configs.py
Accessed 10/15/2020. """

import requests
import json
import base64
from DataSources.configs import CONSUMER_KEY, CONSUMER_SECRET, REFRESH_TOKEN_URL

class Configs:
    def __init__(self):
        self.CONSUMER_KEY = CONSUMER_KEY
        self.CONSUMER_SECRET = CONSUMER_SECRET
        self.BASE_URL="https://api.princeton.edu:443/mobile-app/1.0.0"
        self.COURSE_COURSES="/courses/courses"
        self.COURSE_TERMS="/courses/terms"
        self.REFRESH_TOKEN_URL=REFRESH_TOKEN_URL
        self._refreshToken(grant_type="client_credentials")

    def _refreshToken(self, **kwargs):
        req = requests.post(
            self.REFRESH_TOKEN_URL, 
            data=kwargs, 
            headers={
                "Authorization": "Basic " + base64.b64encode(bytes(self.CONSUMER_KEY + ":" + self.CONSUMER_SECRET, "utf-8")).decode("utf-8")
            },
        )
        text = req.text
        response = json.loads(text)
        self.ACCESS_TOKEN = response["access_token"]