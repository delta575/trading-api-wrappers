# local
from ..base import Client, Server
from ..common import clean_parameters

# API Server
PROTOCOL = 'https'
HOST = 'api.coinmarketcap.com'
VERSION = 'v1'


class CoinMarketCap(Client):

    def __init__(self, timeout: int=120, retry=None):
        server = Server(PROTOCOL, HOST, VERSION)
        super().__init__(server, timeout, retry)
        self._currencies = None

    def ticker(self,
               currency: str=None,
               convert: str=None,
               start: int=None,
               limit: int=None):
        params = {
            'start': start,
            'limit': limit,
            'convert': convert,
        }
        if currency:
            if len(currency) == 3:
                currency = self._get_symbol(currency)['value']
            data = self.get(f'ticker/{currency}/', params=params)[0]
        else:
            data = self.get('ticker/', params=params)
        return data

    def price(self,
              currency: str,
              convert: str=None):
        ticker = self.ticker(currency, convert)
        return float(ticker[f"price_{convert or 'usd'}".lower()])

    def stats(self, convert: str=None):
        data = self.get('global/', params={'convert': convert})
        return data

    def _get_currencies(self):
        ticker = self.ticker()
        return {currency['symbol']: dict(value=currency['id'], decimals=8)
                for currency in ticker}

    def _get_symbol(self, currency: str):
        if self._currencies is None:
            self._currencies = self._get_currencies()
        return self._currencies[currency.upper()]

    def get(self, endpoint: str, headers: dict=None, params: dict=None):
        clean_params = clean_parameters(params)
        return super().get(endpoint, params=clean_params)
