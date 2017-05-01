from ..base import Server

# API Server
PROTOCOL = 'https'
HOST = 'api.kraken.com'
VERSION = '0'


# Kraken API server
class KrakenServer(Server):

    def __init__(self):
        Server.__init__(self, PROTOCOL, HOST, VERSION)
