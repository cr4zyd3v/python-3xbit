# coding=utf-8
# coding=utf-8
from .enums import *
import time
import requests


class Public:

    def __init__(self):
        self.session = self._init_session()

    def _init_session(self):
        session = requests.session()
        session.headers.update({'Accept': 'application/json'})
        return session


    def _request(self, endpoint, method, params=None, data=None):
        if method == "post":
            r = self.session.post(BASE_URL+endpoint, data=data)
        elif method == "get":
            r = self.session.get(BASE_URL+endpoint, params=params)
        else:
            raise Exception("invalid method")
        return r


    def getTickers(self, conversion=None):
        method = "get"
        if conversion:
            endpoint = "/ticker/{0}/".format(conversion)
        else:
            endpoint = "/ticker/"
        r = self._request(endpoint, method)
        return r.json()


    def getOrderbook(self, primary_pair, secondary_pair, currency_rate=None):
            method = "get"
            endpoint = "/v1/orderbook/{}/{}/".format(primary_pair, secondary_pair)
            payload = {
                "currency_rate": currency_rate
            }
            r = self._request(endpoint, method, params=payload)
            return r.json()


    def getHistory(self, primary_pair, secondary_pair, currency=None, page=None, since=None, until=None):
        method = "get"
        endpoint = "/v1/history/{}/{}/".format(primary_pair, secondary_pair)
        payload = {
            "currency": currency,
            "page": page,
            "since": since,
            "until": until
        }
        r = self._request(endpoint, method, params=payload)
        return r.json()
