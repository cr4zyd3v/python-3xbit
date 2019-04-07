import pysher
import logging

logging.basicConfig(level=logging.ERROR)

class Pusher():
    def __init__(self):
        self.pusher = pysher.Pusher(cluster="us2", key="33bf72c0bab380db4f73")


    def connect(self, orderbook_callback=None, history_callback=None):
        print(1)
        self.pusher.connection.bind('pusher:connection_established', self.connect_handler, orderbook_callback, history_callback)
        self.pusher.connect()


    def connect_handler(self, orderbook_callback, history_callback):
        historyChannel = self.pusher.subscribe('BRL-orderbook-history')
        sellChanell = self.pusher.subscribe('BRL-orderbook-sell')
        buyChannel = self.pusher.subscribe('BRL-orderbook-buy')

        sellChanell.bind('created', orderbook_callback)
        sellChanell.bind('deleted', orderbook_callback)
        sellChanell.bind('updated', orderbook_callback)
        sellChanell.bind('done', orderbook_callback)


        buyChannel.bind('created', orderbook_callback)
        buyChannel.bind('deleted', orderbook_callback)
        buyChannel.bind('updated', orderbook_callback)
        buyChannel.bind('done', orderbook_callback)

        historyChannel.bind("new", history_callback)



