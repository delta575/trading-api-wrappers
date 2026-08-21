"""Mercado Bitcoin public REST client (Brazil, BRL)."""

import time

from ..base import Client, ModelMixin
from ..market import Candlestick, Market, OrderBook, Ticker, Trade
from ..trading import BookQuotationMixin


class MercadoBitcoinPublic(BookQuotationMixin, Client, ModelMixin):
    """Mercado Bitcoin Data API v4."""

    base_url = "https://api.mercadobitcoin.net/api/v4/"
    error_keys = ["message", "error"]

    def markets(self):
        data = self.get("symbols")
        symbols = data.get("symbol") if isinstance(data, dict) else data
        if self.return_json:
            return data
        markets = []
        for symbol in symbols or []:
            parts = str(symbol).split("-", 1)
            base = parts[0] if parts else None
            quote = parts[1] if len(parts) > 1 else None
            markets.append(Market.create(symbol, base, quote, symbol))
        return markets

    def ticker(self, symbol: str = "BTC-BRL"):
        items = self.get("tickers", params={"symbols": str(symbol)})
        data = items[0] if isinstance(items, list) and items else items
        if self.return_json:
            return data
        return Ticker.create(
            data,
            symbol=data.get("pair") or str(symbol),
            last=data.get("last"),
            bid=data.get("buy"),
            ask=data.get("sell"),
            volume=data.get("vol"),
            timestamp=data.get("date"),
        )

    def order_book(self, symbol: str = "BTC-BRL", limit: int | None = 20):
        data = self.get(f"{symbol}/orderbook", params={"limit": limit})
        if self.return_json:
            return data
        return OrderBook.create(data)

    def trades(self, symbol: str = "BTC-BRL", limit: int | None = None):
        items = self.get(f"{symbol}/trades")
        if limit is not None:
            items = items[:limit]
        if self.return_json:
            return items
        return [
            Trade.create(
                item,
                trade_id=item.get("tid"),
                price=item.get("price"),
                amount=item.get("amount"),
                side=item.get("type"),
                timestamp=item.get("date"),
            )
            for item in items
        ]

    def candles(
        self,
        symbol: str = "BTC-BRL",
        resolution: str = "1h",
        to: int | None = None,
        from_time: int | None = None,
    ):
        params = {
            "symbol": str(symbol),
            "resolution": resolution,
            "to": to or int(time.time()),
            "from": from_time or int(time.time()) - 86_400 * 2,
        }
        data = self.get("candles", params=params)
        if self.return_json:
            return data
        stamps = data.get("t") or []
        candles = []
        for i, ts in enumerate(stamps):
            row = {
                "t": ts,
                "o": (data.get("o") or [None])[i] if i < len(data.get("o") or []) else None,
                "h": (data.get("h") or [None])[i] if i < len(data.get("h") or []) else None,
                "l": (data.get("l") or [None])[i] if i < len(data.get("l") or []) else None,
                "c": (data.get("c") or [None])[i] if i < len(data.get("c") or []) else None,
                "v": (data.get("v") or [None])[i] if i < len(data.get("v") or []) else None,
            }
            candles.append(
                Candlestick.create(
                    row,
                    timestamp=ts,
                    open_price=row["o"],
                    high=row["h"],
                    low=row["l"],
                    close=row["c"],
                    volume=row["v"],
                )
            )
        return candles
