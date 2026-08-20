from datetime import datetime

from ..base import Client, ModelMixin
from . import models as _m


class CryptoMKTPublic(Client, ModelMixin):
    """CryptoMarket REST API v3 public client."""

    base_url = "https://api.exchange.cryptomkt.com/api/3/"
    error_keys = ["error", "message"]

    def markets(self, symbols: str | None = None):
        data = self.get("public/symbol", params={"symbols": symbols})
        if self.return_json:
            return data
        return {
            symbol: _m.Market.create_from_json(symbol, info)
            for symbol, info in data.items()
        }

    def ticker(self, symbol: str | None = None):
        endpoint = f"public/ticker/{symbol}" if symbol else "public/ticker"
        data = self.get(endpoint)
        if self.return_json:
            return data
        if symbol:
            return _m.Ticker.create_from_json(str(symbol), data)
        return {
            name: _m.Ticker.create_from_json(name, ticker)
            for name, ticker in data.items()
        }

    def order_book(self, symbol: str, depth: int | None = None):
        data = self.get(
            f"public/orderbook/{symbol}",
            params={"depth": depth},
        )
        if self.return_json:
            return data
        return _m.OrderBook.create_from_json(data)

    def trades(
        self,
        symbol: str,
        limit: int | None = None,
        sort: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
    ):
        params = {
            "limit": limit,
            "sort": sort,
        }
        if isinstance(since, datetime):
            params["from"] = since.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        if isinstance(until, datetime):
            params["till"] = until.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        data = self.get(f"public/trades/{symbol}", params=params)
        if self.return_json:
            return data
        return [_m.Trade.create_from_json(trade) for trade in data]
