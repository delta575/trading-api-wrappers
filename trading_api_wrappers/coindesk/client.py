from datetime import datetime, timedelta

from ..base import Client
from ..common import current_utc_date, date_range


class CoinDesk(Client):
    base_url = "http://api.coindesk.com/v1/"
    timeout = 15

    def bpi(self, currency: str):
        return _BPI(self, currency)

    def rate(self, currency: str):
        return _Rate(self, currency)


class _BPI(CoinDesk):
    def __init__(self, parent, currency: str):
        super().__init__(timeout=parent.timeout)
        self.currency = currency.upper()

    def current(self):
        return self.get(f"bpi/currentprice/{self.currency}.json")

    def historical(
        self, start: datetime, end: datetime = None, include_today: bool = False
    ):
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
            current["bpi"] = {str(today): current["bpi"][self.currency]["rate_float"]}
            return current
        # Normal call for historical BPI
        response = self.get(
            "bpi/historical/close.json",
            params={
                "currency": self.currency,
                "start": start,
                "end": end,
            },
        )
        # If end date is today, add current BPI
        if end == today and include_today:
            response["bpi"][str(today)] = self.rate(self.currency).current()
        # Validate response
        historical_bpi = response["bpi"]
        for d in date_range(start, end):
            assert historical_bpi[str(d)], f"{d} is not present in BPI!"

        return response

    @staticmethod
    def _validate_historical_date(date):
        if not date:
            return
        current_date = current_utc_date()
        msg = f"({date}) must be a date <= current date " f"({current_date})"
        assert date <= current_date, msg


class _Rate(CoinDesk):
    def __init__(self, parent, currency: str):
        super().__init__(timeout=parent.timeout)
        self.currency = currency.upper()
        self._bpi = self.bpi(self.currency)

    def current(self):
        response = self._bpi.current()
        rate = response["bpi"][self.currency]["rate_float"]
        return rate

    def historical(
        self, start: datetime, end: datetime = None, include_today: bool = False
    ):
        response = self._bpi.historical(start, end, include_today)
        rate_dict = response["bpi"]
        return rate_dict

    def for_date(self, date_for: datetime):
        if isinstance(date_for, datetime):
            date_for = date_for.date()
        rate_dict = self.historical(start=date_for, end=date_for)
        rate = rate_dict[str(date_for)]
        return rate

    def since_date(self, date_since: datetime, include_today: bool = False):
        if isinstance(date_since, datetime):
            date_since = date_since.date()
        rate_dict = self.historical(date_since, None, include_today)
        return rate_dict

    def last_n_days(self, n_days: int, include_today: bool = False):
        start = current_utc_date() - timedelta(days=n_days)
        rate_dict = self.historical(start, None, include_today)
        return rate_dict
