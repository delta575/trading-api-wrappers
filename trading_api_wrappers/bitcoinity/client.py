# local
from ..base import Client, Server

# API Server
PROTOCOL = 'https'
HOST = 'bitcoinity.org'
VERSION = ''

# API Paths
PATH_TICKER = 'markets/get_ticker'


class Bitcoinity(Client):
    def __init__(self, timeout=15):
        server = Server(PROTOCOL, HOST, VERSION)
        Client.__init__(self, server, timeout)

    def ticker(self, currency, exchange, span):
        parameters = {
            'currency': currency,
            'exchange': exchange,
            'span': span
        }
        url = self.url_for(PATH_TICKER)
        return self.get(url, params=parameters)
