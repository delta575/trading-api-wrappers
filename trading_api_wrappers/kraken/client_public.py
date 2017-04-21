# local
from trading_api_wrappers.base import Client
from .constants import KrakenServer

# API Paths
PATH_SERVER_TIME = 'public/Time'
PATH_ASSETS = 'public/Assets'
PATH_ASSET_PAIRS = 'public/AssetPairs'
PATH_TICKER = 'public/Ticker'
PATH_OHCL = 'public/OHCL'
PATH_ORDER_BOOK = 'public/Depth'
PATH_TRADES = 'public/Trades'
PATH_SPREAD = 'public/Spread'



class KrakenPublic(Client):

    def __init__(self, timeout=30):
        Client.__init__(self, KrakenServer(), timeout)

    def server_time(self):
        url = self.url_for(PATH_SERVER_TIME)
        return self.get(url)

    def assets(self):
        url = self.url_for(PATH_ASSETS)
        return self.get(url)

    def asset_pairs(self):
        url = self.url_for(PATH_ASSET_PAIRS)
        return self.get(url)

    def ticker(self, symbol):
        parameters = {'pair': symbol}
        url = self.url_for(PATH_TICKER)
        return self.get(url, params=parameters)

    def ohcl(self, symbol, interval=None, since=None):
        parameters = {
            'pair': symbol,
            'interval': interval,
            'since': since
        }
        url = self.url_for(PATH_OHCL)
        return self.get(url, params=parameters)

    def order_book(self, symbol, count=None):
        parameters = {
            'pair': symbol,
            'count': count
        }
        url = self.url_for(PATH_ORDER_BOOK)
        return self.get(url, params=parameters)

    def trades(self, symbol, since=None):
        parameters = {
            'pair': symbol,
            'since': since
        }
        url = self.url_for(PATH_TRADES)
        return self.get(url, params=parameters)

    def spread(self, symbol, since=None):
        parameters = {
            'pair': symbol,
            'since': since
        }
        url = self.url_for(PATH_SPREAD)
        return self.get(url, params=parameters)