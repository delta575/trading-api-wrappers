from ..base import Server

# API Server
PROTOCOL = 'https'
HOST = 'api.bitfinex.com'


# Bitfinex API server
class BitfinexServer(Server):

    def __init__(self, version: int):
        super().__init__(PROTOCOL, HOST, version=f'v{version}')
