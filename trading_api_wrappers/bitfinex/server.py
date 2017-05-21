from ..base import Server

# API Server
PROTOCOL = 'https'
HOST = 'api.bitfinex.com'


# Bitfinex API V1 server
class BitfinexServerV1(Server):

    def __init__(self):
        Server.__init__(self, PROTOCOL, HOST, version='v1')


# Bitfinex API V2 server
class BitfinexServerV2(Server):

    def __init__(self):
        Server.__init__(self, PROTOCOL, HOST, version='v2')