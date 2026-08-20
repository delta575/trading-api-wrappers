"""Coinbase Exchange public REST client (USD book)."""

from ..base import Client, ModelMixin
from ..market import Market, OrderBook, Ticker, Trade


class CoinbasePublic(Client, ModelMixin):
    """Coinbase Exchange (pro) public API, not Advanced Trade retail."""

    base_url = "https://api.exchange.coinbase.com/"
    error_keys = ["message"]

    def markets(self):
        items = self.get("products")
        if self.return_json:
            return items
        return [
            Market.create(
                item.get("id"),
                item.get("base_currency"),
                item.get("quote_currency"),
                item,
            )
            for item in items
        ]

    def ticker(self, product_id: str = "BTC-USD"):
        data = self.get(f"products/{product_id}/ticker")
        if self.return_json:
            return data
        return Ticker.create(
            data,
            symbol=str(product_id),
            last=data.get("price"),
            bid=data.get("bid"),
            ask=data.get("ask"),
            volume=data.get("volume"),
            timestamp=None,
        )

    def order_book(self, product_id: str = "BTC-USD", level: int = 2):
        data = self.get(f"products/{product_id}/book", params={"level": level})
        if self.return_json:
            return data
        return OrderBook.create(data)

    def trades(self, product_id: str = "BTC-USD"):
        items = self.get(f"products/{product_id}/trades")
        if self.return_json:
            return items
        return [
            Trade.create(
                item,
                trade_id=item.get("trade_id"),
                price=item.get("price"),
                amount=item.get("size"),
                side=item.get("side"),
                timestamp=item.get("time"),
            )
            for item in items
        ]
