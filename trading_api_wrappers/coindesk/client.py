from datetime import date, datetime

# local
from trading_api_wrappers.base import Client, Server

# API Server
PROTOCOL = 'https'
HOST = 'api.coindesk.com'
VERSION = 'v1'

# API Paths
PATH_BPI = 'bpi/currentprice/%s.json'
PATH_HISTORICAL = 'bpi/historical/close.json'


class CoinDesk(Client):

    def __init__(self, timeout=15):
        server = Server(PROTOCOL, HOST, VERSION)
        Client.__init__(self, server, timeout)

    def bpi(self, currency):
        return _BPI(self, currency)

    def rate(self, currency):
        return _Rate(self, currency)


class _BPI(CoinDesk):

    def __init__(self, parent, currency):
        super().__init__(timeout=parent.TIMEOUT)
        self.currency = currency.upper()

    def current(self):
        url = self.url_for(PATH_BPI, path_arg=self.currency)
        return self.get(url)

    def historical(self, start=None, end=None):
        parameters = {
            'currency': self.currency,
            'start': start,
            'end': end,
        }
        url = self.url_for(PATH_HISTORICAL)
        return self.get(url, params=parameters)


class _Rate(CoinDesk):

    def __init__(self, parent, currency):
        super().__init__(timeout=parent.TIMEOUT)
        self.currency = currency.upper()
        self._bpi = self.bpi(self.currency)

    def current(self):
        response = self._bpi.current()
        rate = response['bpi'][self.currency]['rate_float']
        return rate

    def historical(self, start=None, end=None):
        response = self._bpi.historical(start=start, end=end)
        rate_dict = response['bpi']
        return rate_dict

    def for_date(self, date_for: date):
        date_now = datetime.utcnow().date()
        if date_for > date_now:
            msg = ('Param date_for must be a date <= the current date '
                   '({0})'.format(date_now))
            raise ValueError(msg)
        if date_for == date_now:
            rate = self.current()
        else:
            rate_dict = self.historical(start=date_for, end=date_for)
            rate = rate_dict[str(date_for)]
        return rate
