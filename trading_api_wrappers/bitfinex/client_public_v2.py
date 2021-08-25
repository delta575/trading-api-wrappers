from datetime import datetime

from . import models_v2 as _m
from ..base import Client, ModelMixin


class BitfinexPublic(Client, ModelMixin):
    base_url = "https://api.bitfinex.com/v2/"
    error_keys = ["message"]

    def ticker(self, symbol: str):
        data = self.get(f"ticker/{symbol}")
        if self.return_json:
            return data
        return _m.TradingTicker.create_from_json(data)

    def tickers(self, symbols: list):
        data = self.get(
            "tickers",
            params={
                "symbols": [str(symbol) for symbol in symbols],
            },
        )
        if self.return_json:
            return data
        return {
            ticker[0]: _m.TradingTicker.create_from_json(ticker[1:]) for ticker in data
        }

    def trades(
        self,
        symbol: str,
        limit: int = None,
        start: float = None,
        end: float = None,
        sort: bool = None,
    ):
        if isinstance(start, datetime):
            start = start.timestamp() * 1000
        if isinstance(end, datetime):
            end = end.timestamp() * 1000
        if sort:
            sort = 1 if sort is True else -1
        data = self.get(
            f"trades/{symbol}/hist",
            params={
                "limit": limit,
                "start": start,
                "end": end,
                "sort": sort,
            },
        )
        if self.return_json:
            return data
        return [_m.TradingTrade.create_from_json(trade) for trade in data]

    def books(self, symbol: str, precision: str, length: int = None):
        data = self.get(f"book/{symbol}/{precision}", params={"len": length})
        if self.return_json:
            return data
        return [_m.TradingBook.create_from_json(book) for book in data]

    def stats(
        self,
        symbol: str,
        key: str,
        size: str,
        side: str,
        section: str,
        sort: bool = None,
    ):
        if sort:
            sort = 1 if sort else -1
        data = self.get(
            f"stats1/{key}:{size}:{symbol}:{side}/{section}", params={"sort": sort}
        )
        if self.return_json:
            return data
        if section == "last":
            return _m.Stat.create_from_json(data)
        else:
            return [_m.Stat.create_from_json(stat) for stat in data]

    def stats_last(
        self, symbol: str, key: str, size: str, side: str, sort: bool = None
    ):
        return self.stats(symbol, key, size, side, "last", sort)

    def stats_hist(
        self, symbol: str, key: str, size: str, side: str, sort: bool = None
    ):
        return self.stats(symbol, key, size, side, "hist", sort)

    def candles(
        self,
        symbol: str,
        section: str,
        time_frame: str,
        limit: int = None,
        start: float = None,
        end: float = None,
        sort: bool = None,
    ):
        if isinstance(start, datetime):
            start = start.timestamp() * 1000
        if isinstance(end, datetime):
            end = end.timestamp() * 1000
        if sort:
            sort = 1 if sort else -1
        data = self.get(
            f"candles/trade:{time_frame}:{symbol}/{section}",
            params={
                "limit": limit,
                "start": start,
                "end": end,
                "sort": sort,
            },
        )
        if self.return_json:
            return data
        if section == "last":
            return _m.Candle.create_from_json(data)
        else:
            return [_m.Candle.create_from_json(candle) for candle in data]

    def candles_last(
        self,
        symbol: str,
        time_frame: str,
        limit: int = None,
        start: float = None,
        end: float = None,
        sort: bool = None,
    ):
        return self.candles(symbol, "last", time_frame, limit, start, end, sort)

    def candles_hist(
        self,
        symbol: str,
        time_frame: str,
        limit: int = None,
        start: float = None,
        end: float = None,
        sort: bool = None,
    ):
        return self.candles(symbol, "hist", time_frame, limit, start, end, sort)
