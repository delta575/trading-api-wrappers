from ..auth import ApiKeyAuth
from ..base import AuthMixin, Client
from ..common import format_date_iso


class CurrencyLayer(Client, AuthMixin):
    """CurrencyLayer API Client

    Documentation:
    https://currencylayer.com/documentation
    """

    # https is only enabled for paid subscriptions
    base_url = "http://apilayer.net/api/"
    error_keys = ["error"]
    timeout = 120

    def __init__(self, access_key: str, timeout: int = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.auth = ApiKeyAuth(access_key, api_key_param="access_key")

    def currencies(self):
        """Returns all currently supported currencies.

        Returns:
            dict:
                {
                    "success": true,
                    "terms": "https://currencylayer.com/terms",
                    "privacy": "https://currencylayer.com/privacy",
                    "currencies": {
                        "AED": "United Arab Emirates Dirham",
                        "AFN": "Afghan Afghani",
                        "ALL": "Albanian Lek",
                        "AMD": "Armenian Dram",
                        "ANG": "Netherlands Antillean Guilder",
                        ...
                    }
                }
        """
        return self.get("list")

    def live_rates(self, base: str = None, currencies: list = None):
        """Return real-time exchange rates.

        REQUIRED PLAN: FREE

        Exchange rate data is refreshed every 60 minutes for Free & Basic
        plans, every 10 minutes for Professional, and every 60 seconds for
        Enterprise.

        Both free and paid users may access real-time exchange rates.
        Optionally, it is possible to define an additional base currency,
        or specific output currencies using the currencies parameter.

        Args:
            base (str):
                REQUIRED PLAN: BASIC
                Request exchange rates relative to a different base currency
                (default is USD).
            currencies (list):
                Limit the request to a set of specific currencies codes.

        Returns:
            dict:
                {
                    "success": true,
                    "terms": "https://currencylayer.com/terms",
                    "privacy": "https://currencylayer.com/privacy",
                    "timestamp": 1432400348,
                    "source": "USD",
                    "quotes": {
                        "USDAUD": 1.278342,
                        "USDEUR": 0.908019,
                        "USDGBP": 0.645558,
                        "USDPLN": 3.731504,
                        ...
                    }
                }
        """
        return self.get("live", base, currencies)

    def historical(self, date_for, base: str = None, currencies: list = None):
        """Return historical exchange rates for the date requested.

        REQUIRED PLAN: FREE

        Args:
            date_for: (required)
                Date to return exchange rates for. Accepts `datetime` and `str`
                in ISO format (2000-01-01).
            base (str):
                REQUIRED PLAN: BASIC
                Request exchange rates relative to a different base currency
                (default is USD).
            currencies (list):
                Limit the request to a set of specific currencies codes.

        Returns:
            dict:
                {
                    "success": true,
                    "terms": "https://currencylayer.com/terms",
                    "privacy": "https://currencylayer.com/privacy",
                    "historical": true,
                    "date": "2005-02-01",
                    "timestamp": 1107302399,
                    "source": "USD",
                    "quotes": {
                        "USDAED": 3.67266,
                        "USDALL": 96.848753,
                        "USDAMD": 475.798297,
                        "USDANG": 1.790403,
                        "USDARS": 2.918969,
                        "USDAUD": 1.293878,
                        ...
                    }
                }
        """
        return self.get(
            "historical",
            base,
            currencies,
            params={
                "date": format_date_iso(date_for),
            },
        )

    def time_frame(
        self, start: str, end: str, base: str = None, currencies: list = None
    ):
        """Returns daily historical exchange rates for a time-period.

        (maximum range: 365 days)

        REQUIRED PLAN: PRO

        Args:
            start: (required)
                Start date for the requested time-frame. Accepts `datetime`
                and `str` in ISO format (2000-01-01).
            end: (required)
                End date for the requested time-frame. Accepts `datetime`
                and `str` in ISO format (2000-01-01).
            base (str):
                REQUIRED PLAN: BASIC
                Request exchange rates relative to a different base currency
                (default is USD).
            currencies (list):
                Limit the request to a set of specific currencies codes.

        Returns:
            dict:
                {
                    "success": true,
                    "terms": "https://currencylayer.com/terms",
                    "privacy": "https://currencylayer.com/privacy",
                    "timeframe": true,
                    "start_date": "2010-03-01",
                    "end_date": "2010-04-01",
                    "source": "USD",
                    "quotes": {
                        "2010-03-01": {
                            "USDUSD": 1,
                            "USDGBP": 0.668525,
                            "USDEUR": 0.738541,
                        },
                        "2010-03-02": {
                            "USDUSD": 1,
                            "USDGBP": 0.668827,
                            "USDEUR": 0.736145,
                        },
                        ...
                    },
                }
        """
        return self.get(
            "timeframe",
            base,
            currencies,
            params={
                "start_date": format_date_iso(start),
                "end_date": format_date_iso(end),
            },
        )

    def convert(
        self, amount: float, from_currency: str, to_currency: str, date_for: str = None
    ):
        """Perform a currency conversion for the amount.

        Converts from a `from` currency, to a `to` currency at the latest
        exchange rate. If date_for is passed, the rate for that date will be
        used.

        REQUIRED PLAN: BASIC

        Args:
            amount (float): (required)
                Amount to convert.
            from_currency (str): (required)
                Currency to convert from (the amount's currency).
            to_currency (str): (required)
                Currency to convert to (the return currency).
            date_for:
                End date for the requested time-frame. Accepts `datetime`
                and `str` in ISO format (2000-01-01).
        """
        return self.get(
            "convert",
            params={
                "amount": amount,
                "from": from_currency,
                "to": to_currency,
                "date": format_date_iso(date_for),
            },
        )

    def change(self, base: str = None, currencies: list = None):
        """Return the change (margin and percentage) from yesterday's EOD (End Of Day).

        REQUIRED PLAN: ENTERPRISE

        Args:
            base (str):
                REQUIRED PLAN: BASIC
                Request exchange rates relative to a different base currency
                (default is USD).
            currencies (list):
                Limit the request to a set of specific currencies codes.

        Returns:
            dict:
                {
                    "success": true,
                    "terms": "https://currencylayer.com/terms",
                    "privacy": "https://currencylayer.com/privacy",
                    "change": true,
                    "start_date": "2005-01-01",
                    "end_date": "2010-01-01",
                    "source": "USD",
                    "quotes": {
                        "USDAUD": {
                            "start_rate": 1.281236,
                            "end_rate": 1.108609,
                            "change": -0.1726,
                            "change_pct": -13.4735
                        },
                        "USDEUR": {
                            "start_rate": 0.73618,
                            "end_rate": 0.697253,
                            "change": -0.0389,
                            "change_pct": -5.2877
                        },
                        "USDMXN": {
                            "start_rate": 11.149362,
                            "end_rate": 13.108757,
                            "change": 1.9594,
                            "change_pct": 17.5741,
                        },
                        ...
                    },
                }
        """
        return self.get("change", base, currencies)

    def change_time_frame(
        self, start: str, end: str, base: str = None, currencies: list = None
    ):
        """Return the change (margin and percentage) for a specific time-frame.

        REQUIRED PLAN: ENTERPRISE

        Args:
            start: (required)
                Start date for the requested time-frame. Accepts `datetime`
                and `str` in ISO format (2000-01-01).
            end: (required)
                End date for the requested time-frame. Accepts `datetime`
                and `str` in ISO format (2000-01-01).
            base (str):
                Request exchange rates relative to a different base currency
                (default is USD).
            currencies (list):
                Limit the request to a set of specific currencies codes.

        Returns:
            dict:
                {
                    "success": true,
                    "terms": "https://currencylayer.com/terms",
                    "privacy": "https://currencylayer.com/privacy",
                    "change": true,
                    "start_date": "2005-01-01",
                    "end_date": "2010-01-01",
                    "source": "USD",
                    "quotes": {
                        "USDAUD": {
                            "start_rate": 1.281236,
                            "end_rate": 1.108609,
                            "change": -0.1726,
                            "change_pct": -13.4735
                        },
                        "USDEUR": {
                            "start_rate": 0.73618,
                            "end_rate": 0.697253,
                            "change": -0.0389,
                            "change_pct": -5.2877
                        },
                        "USDMXN": {
                            "start_rate": 11.149362,
                            "end_rate": 13.108757,
                            "change": 1.9594,
                            "change_pct": 17.5741,
                        },
                        ...
                    },
                }
        """
        return self.get(
            "change",
            base,
            currencies,
            params={
                "start": format_date_iso(start),
                "end": format_date_iso(end),
            },
        )

    # OVERRIDES ---------------------------------------------------------------
    def get(
        self,
        endpoint: str,
        base: str = None,
        currencies: list = None,
        params: dict = None,
    ):
        params = params or {}
        if base is not None:
            params["source"] = base
        if isinstance(currencies, list) or isinstance(currencies, tuple):
            currencies = ",".join(currencies)
        if currencies is not None:
            params["currencies"] = currencies
        return super().get(endpoint, params=params)
