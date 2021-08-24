from ..auth import ApiKeyAuth
from ..base import AuthMixin, Client
from ..common import format_date_iso, format_datetime_iso


class OXR(Client, AuthMixin):
    base_url = "https://openexchangerates.org/api/"
    error_keys = ["error"]

    def __init__(self, app_id: str, timeout: int = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.auth = ApiKeyAuth(app_id, api_key_param="app_id")

    def currencies(self):
        """
        Get a JSON list of all currency symbols available from the Open
        Exchange Rates API, along with their full names.
        ref. https://oxr.readme.io/docs/currencies-json
        """
        return self.get("currencies.json")

    def latest(self, base: str = None, symbols: list = None):
        """
        Get latest data.
        ref. https://oxr.readme.io/docs/latest-json
        """
        return self.get("latest.json", base, symbols)

    def historical(self, date_for: str, base: str = None, symbols: list = None):
        """
        Get daily historical data
        ref. https://oxr.readme.io/docs/historical-json
        """
        date_for = format_date_iso(date_for)
        return self.get(f"historical/{date_for}.json", base, symbols)

    def time_series(self, start: str, end: str, base: str = None, symbols: list = None):
        """
        Get time-series data.
        ref. https://oxr.readme.io/docs/time-series-json
        """
        return self.get(
            "time-series.json",
            base,
            symbols,
            params={
                "start": format_date_iso(start),
                "end": format_date_iso(end),
            },
        )

    def convert(self, value: int, from_symbol: str, to_symbol: str):
        """
        Convert any money value from one currency to another at the latest
        API rates.
        ref. https://oxr.readme.io/docs/convert
        """
        return self.get(f"convert/{value}/{from_symbol}/{to_symbol}")

    def ohlc(
        self, start_time: str, period: str, symbols: list = None, base: str = None
    ):
        """
        Get historical open, high, low, close (OHLC) and average data.
        ref. https://oxr.readme.io/docs/ohlc-json
        """
        return self.get(
            "ohlc.json",
            base,
            symbols,
            params={
                "start_time": format_datetime_iso(start_time),
                "period": period,
            },
        )

    # OVERRIDES ---------------------------------------------------------------
    def get(
        self, endpoint: str, base: str = None, symbols: list = None, params: dict = None
    ):
        params = params or {}
        if base is not None:
            params["base"] = base
        if isinstance(symbols, list) or isinstance(symbols, tuple):
            symbols = ",".join(symbols)
        if symbols is not None:
            params["symbols"] = symbols
        return super().get(endpoint, params=params)
