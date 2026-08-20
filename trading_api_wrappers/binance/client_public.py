"""Binance public REST client (spot)."""

from ..base import Client, ModelMixin
from ..market import Market, OrderBook, Ticker, Trade


class BinancePublic(Client, ModelMixin):
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
