from datetime import date, datetime

# local
from ..base import Client, Server

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
        if isinstance(start, datetime):
            start = start.date()
        if isinstance(end, datetime):
            end = end.date()
        date_now = datetime.utcnow().date()
        if start > date_now:
            msg = ("({0}) must be a date <= current date "
                   "({1})".format(start, date_now))
            raise ValueError(msg)
        if start == date_now:
            return {
                'bpi': {
                    str(date_now):
                        self.current()['bpi'][self.currency]['rate_float']
                }
            }
        parameters = {
            'currency': self.currency,
            'start': start,
            'end': end,
        }
        url = self.url_for(PATH_HISTORICAL)
        response = self.get(url, params=parameters)
        if end >= date_now:
            response['bpi'][str(date_now)] = (
                self.current()['bpi'][self.currency]['rate_float'])
        return response


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
        if isinstance(date_for, datetime):
            date_for = date_for.date()
        rate_dict = self.historical(start=date_for, end=date_for)
        rate = rate_dict[str(date_for)]
        return rate
