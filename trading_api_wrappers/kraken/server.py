from ..base import Server

# API Server
PROTOCOL = 'https'
HOST = 'api.kraken.com'
VERSION = '0'


# Kraken API server
class KrakenServer(Server):

    def __init__(self):
        super().__init__(PROTOCOL, HOST, VERSION)
