# local
from ..base import Client, Server
from ..common import clean_parameters

# API Server
PROTOCOL = 'https'
HOST = 'api.coinmarketcap.com'
VERSION = 'v1'

# API Paths
TICKER = 'ticker/'
TICKER_CURRENCY = 'ticker/%s/'
STATS = 'global/'


class CoinMarketCap(Client):

    def __init__(self, timeout=120):
        server = Server(PROTOCOL, HOST, VERSION)
        Client.__init__(self, server, timeout)
        self._currencies = None

    def ticker(self, currency: str=None, convert: str=None,
               start: int=None, limit: int=None):
        params = {
            'start': start,
            'limit': limit,
            'convert': convert,
        }
        if currency:
            if len(currency) == 3:
                currency = self._get_symbol(currency)['value']
            url = self.url_for(TICKER_CURRENCY, path_arg=currency)
            data = self.get(url, params=params)[0]
        else:
            url = self.url_for(TICKER)
            data = self.get(url, params=params)
        return data

    def price(self, currency, convert: str=None):
        ticker = self.ticker(currency, convert)
        return float(ticker['price_{0}'.format(convert or 'usd').lower()])

    def stats(self, convert: str=None):
        params = {
            'convert': convert,
        }
        url = self.url_for(STATS)
        data = self.get(url, params=params)
        return data

    def get(self, url, headers=None, params=None):
        clean_params = clean_parameters(params)
        return super(CoinMarketCap, self).get(url, params=clean_params)

    def _get_currencies(self):
        ticker = self.ticker()
        return {currency['symbol']: dict(value=currency['id'], decimals=8)
                for currency in ticker}

    def _get_symbol(self, currency: str):
        if self._currencies is None:
            self._currencies = self._get_currencies()
        return self._currencies[currency.upper()]
