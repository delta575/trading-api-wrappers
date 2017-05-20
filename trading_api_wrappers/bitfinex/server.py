from ..base import Server

# API Server
PROTOCOL = 'https'
HOST = 'api.bitfinex.com'
VERSION = 'v1'


# Bitfinex API server
class BitfinexServer(Server):

    def __init__(self):
        Server.__init__(self, PROTOCOL, HOST, VERSION)
