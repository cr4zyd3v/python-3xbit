# coding=utf-8
from .enums import *


from requests import get, post
import time


class api3xbit:
    def __init__(self, client_id, client_secret):
        self.__base_url = PUBLIC_BASE_URL
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.access_token = None


    def auth(self):
        endpoint = "/api/oauth/token/"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.__client_id,
            'client_secret': self.__client_secret
        }
        time.sleep(RATE_LIMITER)
        r = post(self.__base_url+endpoint, data=data)
        return r.json()


    def balance(self, currency=None):
        while True:
            if currency:
                endpoint = "/v1/balance/{}".format(currency)
            else:
                endpoint = "/v1/balance/"
            headers = { "Authorization": "Bearer {}".format(self.access_token)}
            r = get(self.__base_url+endpoint, headers=headers)
            if r.status_code == 403:
                time.sleep(RATE_LIMITER)
                self.access_token = self.auth()["access_token"]
                continue
            return r.json()


    def tickers(self, conversion=None):
        if conversion:
            endpoint = "/ticker/{0}/".format(conversion)
        else:
            endpoint = "/ticker/"
        r = get(self.__base_url+endpoint)
        return r.json()


    def orderbook(self, primary_pair, second_pair):
        while True:
            endpoint = "/v1/orderbook/{}/{}/".format(primary_pair, second_pair)
            headers = { "Authorization": "Bearer {}".format(self.access_token)}
            r = get(self.__base_url+endpoint, headers=headers)
            if r.status_code == 403:
                time.sleep(RATE_LIMITER)
                self.access_token = self.auth()["access_token"]
                continue
            return r.json()


print()






#logging.basicConfig(level=logging.ERROR)
api = api3xbit(API_KEYS["client_id"], API_KEYS["client_secret"])
pusher = pysher.Pusher(cluster="us2",
                       key="33bf72c0bab380db4f73")

orderbooks = defaultdict(dict)

def main():

    def created(data):
        data = json.loads(data)
        orderbooks[str(data["unit_price"]["currency"])+"_"+str(data["remaining"]["currency"])][data["order_id"]] = data
    def done(data):
        data = json.loads(data)
        if data["unit_price"]["currency"]+"_"+data["remaining"]["currency"] in orderbooks:
            if data["order_id"] in orderbooks[data["unit_price"]["currency"]+"_"+data["remaining"]["currency"]]:
                orderbooks[data["unit_price"]["currency"]+"_"+data["remaining"]["currency"]].pop(data["order_id"], None)
    def updated(data):
        data = json.loads(data)
        orderbooks[data["unit_price"]["currency"]+"_"+data["remaining"]["currency"]][data["order_id"]] = data
    def deleted(data):
        data = json.loads(data)
        if data["unit_price"]["currency"]+"_"+data["remaining"]["currency"] in orderbooks:
            if data["order_id"] in orderbooks[data["unit_price"]["currency"]+"_"+data["remaining"]["currency"]]:
                orderbooks[data["unit_price"]["currency"]+"_"+data["remaining"]["currency"]].pop(data["order_id"], None)


    # We can't subscribe until we've connected, so we use a callback handler
    # to subscribe when able
    def connect_handler(data):
        #channel1 = pusher.subscribe('BRL-orderbook-history')
        #channel2 = pusher.subscribe('BRL-user-channel-531')
        sellChanell = pusher.subscribe('BRL-orderbook-sell')
        buyChannel = pusher.subscribe('BRL-orderbook-buy')


        sellChanell.bind('created', created)
        sellChanell.bind('deleted', deleted)
        sellChanell.bind('updated', updated)
        sellChanell.bind('done', done)

        buyChannel.bind('created', created)
        buyChannel.bind('deleted', deleted)
        buyChannel.bind('updated', updated)
        buyChannel.bind('done', done)


    pusher.connection.bind('pusher:connection_established', connect_handler)
    pusher.connect()
