"""OKX public REST client."""

from ..base import Client, ModelMixin
from ..errors import InvalidResponse
from ..market import Candlestick, Market, OrderBook, Ticker, Trade
from ..trading import BookQuotationMixin


class OKXPublic(BookQuotationMixin, Client, ModelMixin):
    """OKX REST API v5 public market data."""

    base_url = "https://www.okx.com/api/v5/"
    error_keys = ["msg"]

    def _decode_response(self, response):
        payload = super()._decode_response(response)
        if isinstance(payload, dict) and str(payload.get("code", "0")) != "0":
            raise InvalidResponse(payload.get("msg") or str(payload.get("code")), response)
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    def markets(self, inst_type: str = "SPOT"):
        items = self.get("public/instruments", params={"instType": inst_type})
        if self.return_json:
            return items
        return [
            Market.create(
                item.get("instId"),
                item.get("baseCcy"),
                item.get("quoteCcy"),
                item,
            )
            for item in items
        ]

    def ticker(self, inst_id: str = "BTC-USDT"):
        items = self.get("market/ticker", params={"instId": str(inst_id)})
        data = items[0] if isinstance(items, list) and items else items
        if self.return_json:
            return data
        return Ticker.create(
            data,
            symbol=data.get("instId") or str(inst_id),
            last=data.get("last"),
            bid=data.get("bidPx"),
            ask=data.get("askPx"),
            volume=data.get("vol24h"),
            timestamp=data.get("ts"),
        )

    def order_book(self, inst_id: str = "BTC-USDT", sz: int = 5):
        items = self.get("market/books", params={"instId": str(inst_id), "sz": sz})
        data = items[0] if isinstance(items, list) and items else items
        if self.return_json:
            return data
        return OrderBook.create(data)

    def trades(self, inst_id: str = "BTC-USDT", limit: int = 20):
        items = self.get("market/trades", params={"instId": str(inst_id), "limit": limit})
        if self.return_json:
            return items
        return [
            Trade.create(
                item,
                trade_id=item.get("tradeId"),
                price=item.get("px"),
                amount=item.get("sz"),
                side=item.get("side"),
                timestamp=item.get("ts"),
            )
            for item in items
        ]

    def candles(self, inst_id: str = "BTC-USDT", bar: str = "1H", limit: int = 100):
        rows = self.get(
            "market/candles",
            params={"instId": str(inst_id), "bar": bar, "limit": limit},
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
