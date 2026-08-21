from ..base import Client, ModelMixin
from ..market import Candlestick
from ..trading import BookQuotationMixin


class BitstampPublic(BookQuotationMixin, Client, ModelMixin):
    base_url = "https://www.bitstamp.net/api/"
    error_keys = ["error", "reason"]

    @staticmethod
    def _endpoint_for(endpoint, version=2):
        # NOTE: Bitstamp urls MUST end with /
        if version == 1:
            endpoint = f"{endpoint}/"
        else:
            endpoint = f"v{version}/{endpoint}/"
        return endpoint.lower()

    def ticker(self, currency_pair: str):
        """
        Returns ticker dictionary.
        """
        endpoint = self._endpoint_for(f"ticker/{currency_pair}")
        return self.get(endpoint)

    def ticker_hour(self, currency_pair: str):
        """
        Returns dictionary of the average ticker of the past hour.
        """
        endpoint = self._endpoint_for(f"ticker_hour/{currency_pair}")
        return self.get(endpoint)

    def order_book(self, currency_pair: str):
        """
        Returns dictionary with "bids" and "asks".

        Each is a list of open orders and each order is represented as a list
        of price and amount.
        """
        endpoint = self._endpoint_for(f"order_book/{currency_pair}")
        return self.get(endpoint)

    def transactions(self, currency_pair: str, time_interval: str = None):
        """
        Returns transactions for the last 'timedelta' seconds.

        Parameter time is specified by one of two values of TransRange class.
        """
        params = {"time": str(time_interval)} if time_interval else None
        endpoint = self._endpoint_for(f"transactions/{currency_pair}")
        return self.get(endpoint, params=params)

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
        return self.get(self._endpoint_for("trading-pairs-info"))

    def conversion_rate_usd_eur(self):
        """
        Returns simple dictionary:

            {'buy': 'buy conversion rate', 'sell': 'sell conversion rate'}
        """
        endpoint = self._endpoint_for("eur_usd")
        return self.get(endpoint)

    def markets(self):
        return self.trading_pairs_info()

    def trades(self, currency_pair: str, time_interval: str = None):
        return self.transactions(currency_pair, time_interval)

    def candles(
        self,
        currency_pair: str,
        step: int = 3600,
        limit: int = 100,
        start: int = None,
        end: int = None,
    ):
        endpoint = self._endpoint_for(f"ohlc/{currency_pair}")
        data = self.get(
            endpoint,
            params={
                "step": step,
                "limit": limit,
                "start": start,
                "end": end,
            },
        )
        if self.return_json:
            return data
        rows = (
            (data.get("data") or {}).get("ohlc") if isinstance(data, dict) else None
        ) or []
        return [
            Candlestick.create(
                row,
                timestamp=int(row["timestamp"]) if row.get("timestamp") else None,
                open_price=row.get("open"),
                high=row.get("high"),
                low=row.get("low"),
                close=row.get("close"),
                volume=row.get("volume"),
            )
            for row in rows
        ]
