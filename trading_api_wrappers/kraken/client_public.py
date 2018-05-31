# local
from .server import KrakenServer
from ..base import Client


class KrakenPublic(Client):

    error_key = 'error'

    def __init__(self, timeout: int=30, retry=None):
        super().__init__(KrakenServer(), timeout, retry)

    def server_time(self):
        url = self.url_for('public/Time')
        return self.get(url)

    def assets(self):
        url = self.url_for('public/Assets')
        return self.get(url)

    def asset_pairs(self):
        url = self.url_for('public/AssetPairs')
        return self.get(url)

    def ticker(self, symbol: str):
        params = {
            'pair': str(symbol),
        }
        url = self.url_for('public/Ticker')
        return self.get(url, params=params)

    def ohcl(self,
             symbol: str,
             interval: int=None,
             since: str=None):
        params = {
            'pair': str(symbol),
            'interval': interval,
            'since': since,
        }
        url = self.url_for('public/OHCL')
        return self.get(url, params=params)

    def order_book(self,
                   symbol: str,
                   count: int=None):
        params = {
            'pair': str(symbol),
            'count': count,
        }
        url = self.url_for('public/Depth')
        return self.get(url, params=params)

    def trades(self,
               symbol: str,
               since: str=None):
        params = {
            'pair': str(symbol),
            'since': since,
        }
        url = self.url_for('public/Trades')
        return self.get(url, params=params)

    def spread(self,
               symbol: str,
               since: str=None):
        params = {
            'pair': str(symbol),
            'since': since,
        }
        url = self.url_for('public/Spread')
        return self.get(url, params=params)
