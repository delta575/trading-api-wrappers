from datetime import datetime, timedelta

# local
from ..base import Client, Server
from ..common import current_utc_date, date_range

# API Server
PROTOCOL = 'http'
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

    def historical(self, start, end=None, include_today=False):
        if isinstance(start, datetime):
            start = start.date()
        if isinstance(end, datetime):
            end = end.date()
        today = current_utc_date()
        end = end or today
        # Validate dates
        assert start <= end, "'start' date must <= 'end' date'!"
        self._validate_historical_date(start)
        self._validate_historical_date(end)
        # If start date is today, return only current BPI
        if start == today:
            current = self.bpi(self.currency).current()
            current['bpi'] = {
                str(today): current['bpi'][self.currency]['rate_float']}
            return current
        # Normal call for historical BPI
        parameters = {
            'currency': self.currency,
            'start': start,
            'end': end,
        }
        url = self.url_for(PATH_HISTORICAL)
        response = self.get(url, params=parameters)
        # If end date is today, add current BPI
        if end == today and include_today:
            response['bpi'][str(today)] = (
                self.rate(self.currency).current())
        # Validate response
        historical_bpi = response['bpi']
        for d in date_range(start, end):
            assert historical_bpi[str(d)], (
                '{0} is not present in BPI!'.format(d))

        return response

    def _validate_historical_date(self, date):
        if not date:
            return
        current_date = current_utc_date()
        msg = ("({0}) must be a date <= current date "
               "({1})".format(date, current_date))
        assert date <= current_date, msg


class _Rate(CoinDesk):
    def __init__(self, parent, currency):
        super().__init__(timeout=parent.TIMEOUT)
        self.currency = currency.upper()
        self._bpi = self.bpi(self.currency)

    def current(self):
        response = self._bpi.current()
        rate = response['bpi'][self.currency]['rate_float']
        return rate

    def historical(self, start, end=None, include_today=False):
        response = self._bpi.historical(
            start=start, end=end, include_today=include_today)
        rate_dict = response['bpi']
        return rate_dict

    def for_date(self, date_for):
        if isinstance(date_for, datetime):
            date_for = date_for.date()
        rate_dict = self.historical(start=date_for, end=date_for)
        rate = rate_dict[str(date_for)]
        return rate

    def since_date(self, date_since, include_today=False):
        if isinstance(date_since, datetime):
            date_since = date_since.date()
        rate_dict = self.historical(
            start=date_since, end=None, include_today=include_today)
        return rate_dict

    def last_n_days(self, n_days, include_today=False):
        start = current_utc_date() - timedelta(days=n_days)
        rate_dict = self.historical(
            start=start, end=None, include_today=include_today)
        return rate_dict
