# local
from ..base import Client, Server
from ..common import format_date_iso, format_datetime_iso

# API Server
PROTOCOL = 'https'
HOST = 'openexchangerates.org/api/'

# API Paths
CURRENCIES = 'currencies.json'
LATEST = 'latest.json'
HISTORICAL = 'historical/%s.json'
TIME_SERIES = 'time-series.json'
CONVERT = 'convert/%s/%s/%s'
OHLC = 'ohlc.json'


class OXR(Client):

    error_key = 'error'

    def __init__(self, app_id: str, timeout: int=120):
        server = Server(PROTOCOL, HOST)
        Client.__init__(self, server, timeout)
        self.APP_ID = str(app_id)

    def currencies(self):
        """
        Get a JSON list of all currency symbols available from the Open
        Exchange Rates API, along with their full names.
        ref. https://oxr.readme.io/docs/currencies-json
        """
        url = self.url_for(CURRENCIES)
        data = self.get(url)
        return data

    def latest(self, 
               base: str=None, 
               symbols: list=None):
        """
        Get latest data.
        ref. https://oxr.readme.io/docs/latest-json
        """
        url = self.url_for(LATEST)
        data = self._get_exchange_rates(url, base, symbols)
        return data

    def historical(self,
                   date_for: str,
                   base: str=None, 
                   symbols: list=None):
        """
        Get daily historical data
        ref. https://oxr.readme.io/docs/historical-json
        """
        date_for = format_date_iso(date_for)
        url = self.url_for(HISTORICAL, path_arg=date_for)
        data = self._get_exchange_rates(url, base, symbols)
        return data

    def time_series(self,
                    start: str,
                    end: str,
                    base: str=None, 
                    symbols: list=None):
        """
        Get time-series data.
        ref. https://oxr.readme.io/docs/time-series-json
        """
        params = {
            'start': format_date_iso(start),
            'end': format_date_iso(end),
        }
        url = self.url_for(TIME_SERIES)
        data = self._get_exchange_rates(url, base, symbols, params)
        return data

    def convert(self,
                value: int,
                from_symbol: str,
                to_symbol: str):
        """
        Convert any money value from one currency to another at the latest
        API rates.
        ref. https://oxr.readme.io/docs/convert
        """
        url = self.url_for(CONVERT, path_arg=(value, from_symbol, to_symbol))
        data = self._get_exchange_rates(url)
        return data

    def ohlc(self,
             start_time: str,
             period: str,
             symbols: list=None,
             base: str=None):
        """
        Get historical open, high, low, close (OHLC) and average data.
        ref. https://oxr.readme.io/docs/ohlc-json
        """
        params = {
            'start_time': format_datetime_iso(start_time),
            'period': period,
        }
        url = self.url_for(OHLC)
        data = self._get_exchange_rates(url, base, symbols, params)
        return data

    def _get_exchange_rates(self,
                            url: str,
                            base: str=None,
                            symbols: list=None,
                            params: dict=None):
        if params is None:
            params = dict()
        params['app_id'] = self.APP_ID
        if base is not None:
            params['base'] = base
        if isinstance(symbols, list) or isinstance(symbols, tuple):
            symbols = ','.join(symbols)
        if symbols is not None:
            params['symbols'] = symbols
        return self.get(url, params=params)
