"""Binance public REST client (spot)."""

from ..base import Client, ModelMixin
from ..market import Candlestick, Market, OrderBook, Ticker, Trade
from ..trading import BookQuotationMixin


class BinancePublic(BookQuotationMixin, Client, ModelMixin):
    """Binance Spot REST API v3."""

    base_url = "https://api.binance.com/api/v3/"
    error_keys = ["msg"]

    def markets(self):
        data = self.get("exchangeInfo")
        items = data.get("symbols") if isinstance(data, dict) else data
        if self.return_json:
            return data
        markets = []
        for item in items or []:
            markets.append(
                Market.create(
                    item.get("symbol"),
                    item.get("baseAsset"),
                    item.get("quoteAsset"),
                    item,
                )
            )
        return markets

    def ticker(self, symbol: str = "BTCUSDT"):
        data = self.get("ticker/24hr", params={"symbol": str(symbol)})
        if self.return_json:
            return data
        return Ticker.create(
            data,
            symbol=data.get("symbol") or str(symbol),
            last=data.get("lastPrice"),
            bid=data.get("bidPrice"),
            ask=data.get("askPrice"),
            volume=data.get("volume"),
            timestamp=data.get("closeTime"),
        )

    def order_book(self, symbol: str = "BTCUSDT", limit: int = 20):
        data = self.get("depth", params={"symbol": str(symbol), "limit": limit})
        if self.return_json:
            return data
        return OrderBook.create(data)

    def trades(self, symbol: str = "BTCUSDT", limit: int = 20):
        items = self.get("trades", params={"symbol": str(symbol), "limit": limit})
        if self.return_json:
            return items
        return [
            Trade.create(
                item,
                trade_id=item.get("id"),
                price=item.get("price"),
                amount=item.get("qty"),
                side="sell" if item.get("isBuyerMaker") else "buy",
                timestamp=item.get("time"),
            )
            for item in items
        ]

    def candles(self, symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 100):
        rows = self.get(
            "klines",
            params={"symbol": str(symbol), "interval": interval, "limit": limit},
        )
        if self.return_json:
            return rows
        return [
            Candlestick.create(
                row,
                timestamp=row[0],
                open_price=row[1],
                high=row[2],
                low=row[3],
                close=row[4],
                volume=row[5],
            )
            for row in rows
        ]
