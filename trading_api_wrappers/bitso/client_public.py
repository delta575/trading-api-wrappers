"""Bitso public REST client (Mexico, MXN)."""

from ..base import Client, ModelMixin
from ..errors import InvalidResponse
from ..market import Candlestick, Market, OrderBook, Ticker, Trade
from ..trading import BookQuotationMixin


class BitsoPublic(BookQuotationMixin, Client, ModelMixin):
    """Bitso public trading API v3."""

    base_url = "https://api.bitso.com/api/v3/"
    error_keys = ["error", "message"]

    def _decode_response(self, response):
        payload = super()._decode_response(response)
        if isinstance(payload, dict) and payload.get("success") is False:
            error = payload.get("error") or payload
            raise InvalidResponse(str(error), response)
        if isinstance(payload, dict) and "payload" in payload:
            return payload["payload"]
        return payload

    def markets(self):
        items = self.get("available_books/")
        if self.return_json:
            return items
        markets = []
        for item in items:
            book = item.get("book", "")
            parts = str(book).split("_", 1)
            base = parts[0].upper() if parts else None
            quote = parts[1].upper() if len(parts) > 1 else None
            markets.append(Market.create(book, base, quote, item))
        return markets

    def ticker(self, book: str = "btc_mxn"):
        data = self.get("ticker/", params={"book": str(book)})
        if self.return_json:
            return data
        return Ticker.create(
            data,
            symbol=data.get("book") or str(book),
            last=data.get("last"),
            bid=data.get("bid"),
            ask=data.get("ask"),
            volume=data.get("volume"),
            timestamp=None,
        )

    def order_book(self, book: str = "btc_mxn", aggregate: bool | None = None):
        data = self.get(
            "order_book/",
            params={"book": str(book), "aggregate": aggregate},
        )
        if self.return_json:
            return data
        return OrderBook.create(data, timestamp=data.get("updated_at"))

    def trades(self, book: str = "btc_mxn", limit: int = 25):
        items = self.get("trades/", params={"book": str(book), "limit": limit})
        if self.return_json:
            return items
        return [
            Trade.create(
                item,
                trade_id=item.get("tid"),
                price=item.get("price"),
                amount=item.get("amount"),
                side=item.get("maker_side") or item.get("side"),
                timestamp=item.get("created_at"),
            )
            for item in items
        ]

    def candles(self, book: str = "btc_mxn", time_bucket: int = 3600):
        items = self.get(
            "ohlc/",
            params={"book": str(book), "time_bucket": time_bucket},
        )
        if self.return_json:
            return items
        return [
            Candlestick.create(
                item,
                timestamp=item.get("bucket_start_time"),
                open_price=item.get("first_rate"),
                high=item.get("max_rate"),
                low=item.get("min_rate"),
                close=item.get("last_rate"),
                volume=item.get("volume"),
            )
            for item in items
        ]
