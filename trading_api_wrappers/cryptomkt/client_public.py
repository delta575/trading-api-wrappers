from datetime import datetime
from typing import List

from . import constants as _c
from . import models as _m
from ..base import Client, ModelMixin


class CryptoMKTPublic(Client, ModelMixin):
    base_url = "https://api.exchange.cryptomkt.com/api/3/public/"
    error_keys = ["message"]

    def markets(self):
        data = self.get("symbol")
        return data

    def ticker(self, market_id: str):
        data = self.get("ticker")
        if self.return_json:
            return data[market_id]
        return _m.Ticker.create_from_json([data[market_id]])

    def order_book(
        self,
        market_id: str,
        volume: int = None,
        depth: int = None,
    ): 
        data = self.get(
            f"orderbook/{market_id}",
            params={
                "volume": volume,
                "depth": depth,
            },
        )
        if self.return_json:
            return data
        return _m.OrderBook.create_from_json(data)

    def trades(
        self,
        market_id: str,
        start: datetime = None,
        end: datetime = None,
        by: str = 'timestamp',
        sort: str = 'DESC',
        limit: int = _c.ORDERS_LIMIT,
        offset: int = _c.ORDERS_LIMIT,
    ):
        if isinstance(start, datetime):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, datetime):
            end = end.strftime("%Y-%m-%d")
        data = self.get(
            f"trades/{str(market_id)}",
            params={
                "from": start,
                "till": end,
                "by": by,
                "sort": sort,
                "limit": limit,
                "offset": offset,
            },
        )
        if self.return_json:
            return data
        return _m.Trades.create_from_json(data)
