from ..base import Client, ModelMixin
from ..market import Candlestick, Market
from ..trading import BookQuotationMixin


class KrakenPublic(BookQuotationMixin, Client, ModelMixin):
    base_url = "https://api.kraken.com/0/"
    error_keys = ["error"]

    def server_time(self):
        return self.get("public/Time")

    def assets(self):
        return self.get("public/Assets")

    def asset_pairs(self):
        return self.get("public/AssetPairs")

    def markets(self):
        data = self.asset_pairs()
        result = data.get("result") if isinstance(data, dict) else data
        if self.return_json:
            return data
        markets = []
        for pair, info in (result or {}).items():
            markets.append(
                Market.create(
                    info.get("altname") or pair,
                    info.get("base"),
                    info.get("quote"),
                    info,
                )
            )
        return markets

    def ticker(self, symbol: str):
        return self.get(
            "public/Ticker",
            params={
                "pair": str(symbol),
            },
        )

    def ohlc(self, symbol: str, interval: int = None, since: str = None):
        return self.get(
            "public/OHLC",
            params={
                "pair": str(symbol),
                "interval": interval,
                "since": since,
            },
        )

    def candles(self, symbol: str, interval: int = 60, since: str = None):
        data = self.ohlc(symbol, interval=interval, since=since)
        if self.return_json:
            return data
        result = data.get("result") if isinstance(data, dict) else data
        rows = []
        if isinstance(result, dict):
            for key, value in result.items():
                if key == "last" or not isinstance(value, list):
                    continue
                rows = value
                break
        candles = []
        for row in rows:
            candles.append(
                Candlestick.create(
                    row,
                    timestamp=row[0],
                    open_price=row[1],
                    high=row[2],
                    low=row[3],
                    close=row[4],
                    volume=row[6] if len(row) > 6 else None,
                )
            )
        return candles

    def order_book(self, symbol: str, count: int = None):
        return self.get(
            "public/Depth",
            params={
                "pair": str(symbol),
                "count": count,
            },
        )

    def trades(self, symbol: str, since: str = None):
        return self.get(
            "public/Trades",
            params={
                "pair": str(symbol),
                "since": since,
            },
        )

    def spread(self, symbol: str, since: str = None):
        return self.get(
            "public/Spread",
            params={
                "pair": str(symbol),
                "since": since,
            },
        )
