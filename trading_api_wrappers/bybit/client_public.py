"""Bybit public REST client (spot)."""

from ..base import Client, ModelMixin
from ..errors import InvalidResponse
from ..market import Candlestick, Market, OrderBook, Ticker, Trade
from ..trading import BookQuotationMixin


class BybitPublic(BookQuotationMixin, Client, ModelMixin):
    """Bybit v5 public market data. Defaults to spot."""

    base_url = "https://api.bybit.com/v5/"
    error_keys = []
    category = "spot"

    def _decode_response(self, response):
        payload = super()._decode_response(response)
        if isinstance(payload, dict) and payload.get("retCode") not in (0, "0", None):
            raise InvalidResponse(payload.get("retMsg") or str(payload.get("retCode")), response)
        if isinstance(payload, dict) and "result" in payload:
            return payload["result"]
        return payload

    def markets(self, category: str | None = None):
        data = self.get(
            "market/instruments-info",
            params={"category": category or self.category},
        )
        items = data.get("list") if isinstance(data, dict) else data
        if self.return_json:
            return data
        return [
            Market.create(
                item.get("symbol"),
                item.get("baseCoin"),
                item.get("quoteCoin"),
                item,
            )
            for item in items or []
        ]

    def ticker(self, symbol: str = "BTCUSDT", category: str | None = None):
        data = self.get(
            "market/tickers",
            params={"category": category or self.category, "symbol": str(symbol)},
        )
        items = data.get("list") if isinstance(data, dict) else data
        item = items[0] if isinstance(items, list) and items else items
        if self.return_json:
            return item
        return Ticker.create(
            item,
            symbol=item.get("symbol") or str(symbol),
            last=item.get("lastPrice"),
            bid=item.get("bid1Price"),
            ask=item.get("ask1Price"),
            volume=item.get("volume24h"),
            timestamp=data.get("ts") if isinstance(data, dict) else None,
        )

    def order_book(
        self, symbol: str = "BTCUSDT", limit: int = 25, category: str | None = None
    ):
        data = self.get(
            "market/orderbook",
            params={
                "category": category or self.category,
                "symbol": str(symbol),
                "limit": limit,
            },
        )
        if self.return_json:
            return data
        return OrderBook.create(data)

    def trades(
        self, symbol: str = "BTCUSDT", limit: int = 20, category: str | None = None
    ):
        data = self.get(
            "market/recent-trade",
            params={
                "category": category or self.category,
                "symbol": str(symbol),
                "limit": limit,
            },
        )
        items = data.get("list") if isinstance(data, dict) else data
        if self.return_json:
            return items
        return [
            Trade.create(
                item,
                trade_id=item.get("execId"),
                price=item.get("price"),
                amount=item.get("size"),
                side=item.get("side"),
                timestamp=item.get("time"),
            )
            for item in items or []
        ]

    def candles(
        self,
        symbol: str = "BTCUSDT",
        interval: str = "60",
        limit: int = 100,
        category: str | None = None,
    ):
        data = self.get(
            "market/kline",
            params={
                "category": category or self.category,
                "symbol": str(symbol),
                "interval": interval,
                "limit": limit,
            },
        )
        rows = data.get("list") if isinstance(data, dict) else data
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
            for row in rows or []
        ]
