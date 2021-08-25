from . import models as _m
from ..base import Client, ModelMixin


class BitexPublic(Client, ModelMixin):
    """Bitex API Doc: https://bitex.la/developers"""

    base_url = "https://bitex.la/api-v1/rest/"
    error_keys = ["error"]

    def ticker(self, market_id: str):
        """Overview of current market prices and trade volume."""
        data = self.get(f"{market_id}/market/ticker")
        if self.return_json:
            return data
        return _m.Ticker.create_from_json(data)

    def order_book(self, market_id: str):
        """Return bids and asks represented as a list of price and amount."""
        data = self.get(f"{market_id}/market/order_book")
        if self.return_json:
            return data
        return _m.OrderBook.create_from_json(data)

    def _transactions(self, market_id: str, endpoint: str):
        data = self.get(f"{market_id}/market/{endpoint}")
        if self.return_json:
            return data
        return [_m.Transaction.create_from_json(tx) for tx in data]

    def transactions(self, market_id: str):
        """
        Return a list representing all individual trades for the past 60
        minutes, sorted by descending date.
        """
        return self._transactions(market_id, "transactions")

    def transactions_archive(self, market_id: str):
        """
        Return a list representing all individual trades that took place
        since Bitex started trading until the beginning of the current hour,
        sorted by descending date.

        This is a large download, so Bitex only allows to retrieve it a few
        times per hour. Don't worry though, it only changes once an hour.
        """
        return self._transactions(market_id, "transactions_archive")
