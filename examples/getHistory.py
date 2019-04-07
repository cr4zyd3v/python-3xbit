import pysher


def haddler(data):
    print(data)


def connect_handler(data):
    #channel1 = pusher.subscribe('BRL-orderbook-history')
    #channel2 = pusher.subscribe('BRL-user-channel-531')
    sellChanell = pusher.subscribe('BRL-orderbook-sell')
    buyChannel = pusher.subscribe('BRL-orderbook-buy')


    sellChanell.bind('created', haddler)
    sellChanell.bind('deleted', haddler)
    sellChanell.bind('updated', haddler)
    sellChanell.bind('done', haddler)

    buyChannel.bind('created', haddler)
    buyChannel.bind('deleted', haddler)
    buyChannel.bind('updated', haddler)
    buyChannel.bind('done', haddler)

pusher = pysher.Pusher(cluster="us2",
                       key="33bf72c0bab380db4f73")
pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()
