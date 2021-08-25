from datetime import datetime

from . import constants as _c
from . import models as _m
from ..base import Client, ModelMixin


class CryptoMKTPublic(Client, ModelMixin):
    base_url = "https://api.cryptomkt.com/v1/"
    error_keys = ["message"]

    def markets(self):
        data = self.get("market")
        return data["data"]

    def ticker(self, market_id: str):
        data = self.get("ticker", params={"market": str(market_id)})
        if self.return_json:
            return data
        return _m.Ticker.create_from_json(data["data"])

    def order_book(
        self,
        market_id: str,
        order_type: str,
        page: int = None,
        limit: int = _c.ORDERS_LIMIT,
    ):
        data = self.get(
            "book",
            params={
                "market": str(market_id),
                "type": str(order_type),
                "page": page,
                "limit": limit,
            },
        )
        if self.return_json:
            return data
        return _m.OrderBook.create_from_json(data["data"], data["pagination"])

    def trades(
        self,
        market_id: str,
        start: datetime = None,
        end: datetime = None,
        page: int = None,
        limit: int = _c.ORDERS_LIMIT,
    ):
        if isinstance(start, datetime):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, datetime):
            end = end.strftime("%Y-%m-%d")
        data = self.get(
            "trades",
            params={
                "market": str(market_id),
                "start": start,
                "end": end,
                "page": page,
                "limit": limit,
            },
        )
        if self.return_json:
            return data
        return _m.Trades.create_from_json(data["data"], data.get("pagination"))
