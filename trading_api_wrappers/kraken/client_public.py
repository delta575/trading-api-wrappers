# local
from . import constants as _c
from ..base import Client
from .server import KrakenServer

_p = _c.Path


class KrakenPublic(Client):

    error_key = 'error'

    def __init__(self, timeout=30):
        Client.__init__(self, KrakenServer(), timeout)

    def server_time(self):
        url = self.url_for(_p.SERVER_TIME)
        return self.get(url)

    def assets(self):
        url = self.url_for(_p.ASSETS)
        return self.get(url)

    def asset_pairs(self):
        url = self.url_for(_p.ASSET_PAIRS)
        return self.get(url)

    def ticker(self, symbol):
        parameters = {'pair': symbol}
        url = self.url_for(_p.TICKER)
        return self.get(url, params=parameters)

    def ohcl(self, symbol, interval=None, since=None):
        parameters = {
            'pair': symbol,
            'interval': interval,
            'since': since
        }
        url = self.url_for(_p.OHCL)
        return self.get(url, params=parameters)

    def order_book(self, symbol, count=None):
        parameters = {
            'pair': symbol,
            'count': count
        }
        url = self.url_for(_p.ORDER_BOOK)
        return self.get(url, params=parameters)

    def trades(self, symbol, since=None):
        parameters = {
            'pair': symbol,
            'since': since
        }
        url = self.url_for(_p.TRADES)
        return self.get(url, params=parameters)

    def spread(self, symbol, since=None):
        parameters = {
            'pair': symbol,
            'since': since
        }
        url = self.url_for(_p.SPREAD)
        return self.get(url, params=parameters)
