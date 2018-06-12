# local
from .server import KrakenServer
from ..base import Client


class KrakenPublic(Client):
    error_key = 'error'

    def __init__(self, timeout: int=30, retry=None):
        super().__init__(KrakenServer(), timeout, retry)

    def server_time(self):
        return self.get('public/Time')

    def assets(self):
        return self.get('public/Assets')

    def asset_pairs(self):
        return self.get('public/AssetPairs')

    def ticker(self, symbol: str):
        return self.get('public/Ticker', params={
            'pair': str(symbol),
        })

    def ohcl(self,
             symbol: str,
             interval: int=None,
             since: str=None):
        return self.get('public/OHCL', params={
            'pair': str(symbol),
            'interval': interval,
            'since': since,
        })

    def order_book(self,
                   symbol: str,
                   count: int=None):
        return self.get('public/Depth', params={
            'pair': str(symbol),
            'count': count,
        })

    def trades(self,
               symbol: str,
               since: str=None):
        return self.get('public/Trades', params={
            'pair': str(symbol),
            'since': since,
        })

    def spread(self,
               symbol: str,
               since: str=None):
        return self.get('public/Spread', params={
            'pair': str(symbol),
            'since': since,
        })
