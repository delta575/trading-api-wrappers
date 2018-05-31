# local
from .server import BitstampServer
from ..base import Client


class BitstampPublic(Client):

    error_key = 'error'

    def __init__(self, timeout: int=30, retry=None):
        super().__init__(BitstampServer(), timeout, retry)

    def url_for(self, path, path_arg=None, version=2):
        if version == 1:
            url = f'{self.SERVER.URL}/{path}/'
        else:
            url = f'{self.SERVER.URL}/v{version}/{path}/'
        if path_arg:
            url = url % path_arg
        return url

    def ticker(self, currency_pair: str):
        """
        Returns ticker dictionary.
        """
        url = self.url_for('ticker/%s', currency_pair)
        return self.get(url)

    def ticker_hour(self, currency_pair: str):
        """
        Returns dictionary of the average ticker of the past hour.
        """
        url = self.url_for('ticker_hour/%s', currency_pair)
        return self.get(url)

    def order_book(self, currency_pair: str):
        """
        Returns dictionary with "bids" and "asks".

        Each is a list of open orders and each order is represented as a list
        of price and amount.
        """
        url = self.url_for('order_book/%s', currency_pair)
        return self.get(url)

    def transactions(self, currency_pair: str, time_interval: str=None):
        """
        Returns transactions for the last 'timedelta' seconds.

        Parameter time is specified by one of two values of TransRange class.
        """
        params = {'time': str(time_interval)} if time_interval else None
        url = self.url_for('transactions/%s', currency_pair)
        return self.get(url, params=params)

    def trading_pairs_info(self):
        """
        Returns list of dictionaries specifying details of each available
        trading pair:

            {
                'description':'Litecoin / U.S. dollar',
                'name':'LTC/USD',
                'url_symbol':'ltcusd',
                'trading':'Enabled',
                'minimum_order':'5.0 USD',
                'counter_decimals':2,
                'base_decimals':8
            },
        """
        url = self.url_for('trading-pairs-info')
        return self.get(url)

    def conversion_rate_usd_eur(self):
        """
        Returns simple dictionary:

            {'buy': 'buy conversion rate', 'sell': 'sell conversion rate'}
        """
        url = self.url_for('eur_usd', version=1)
        return self.get(url)
