"""Foxbit public REST client (Brazil, BRL + Pix)."""

from ..base import Client, ModelMixin
from ..errors import InvalidResponse
from ..market import Market, OrderBook, Ticker, Trade


class FoxbitPublic(Client, ModelMixin):
    """Foxbit REST API v3 public market data."""

    base_url = "https://api.foxbit.com.br/rest/v3/"
    error_keys = ["message"]

    def _decode_response(self, response):
        payload = super()._decode_response(response)
        if isinstance(payload, dict) and payload.get("error"):
            raise InvalidResponse(str(payload["error"]), response)
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    def markets(self):
        items = self.get("markets")
        if self.return_json:
            return items
        markets = []
        for item in items:
            base = (item.get("base") or {}).get("symbol")
            quote = (item.get("quote") or {}).get("symbol")
            markets.append(
                Market.create(
                    item.get("symbol"),
                    str(base).upper() if base else None,
                    str(quote).upper() if quote else None,
                    item,
                )
            )
        return markets

    def ticker(self, symbol: str = "btcbrl"):
        items = self.get(f"markets/{symbol}/ticker/24hr")
        data = items[0] if isinstance(items, list) and items else items
        if self.return_json:
            return data
        last_trade = data.get("last_trade") or {}
        best = data.get("best") or {}
        rolling = data.get("rolling_24h") or {}
        ask = (best.get("ask") or {}).get("price")
        bid = (best.get("bid") or {}).get("price")
        return Ticker.create(
            data,
            symbol=data.get("market_symbol") or str(symbol),
            last=last_trade.get("price"),
            bid=bid,
            ask=ask,
            volume=rolling.get("volume"),
        )

    def order_book(self, symbol: str = "btcbrl", depth: int = 20):
        data = self.get(f"markets/{symbol}/orderbook", params={"depth": depth})
        if self.return_json:
            return data
        return OrderBook.create(data)

    def trades(self, symbol: str = "btcbrl", page_size: int = 20):
        items = self.get(
            f"markets/{symbol}/trades/history",
            params={"page_size": page_size},
        )
        if self.return_json:
            return items
        return [
            Trade.create(
                item,
                trade_id=item.get("id"),
                price=item.get("price"),
                amount=item.get("volume"),
                side=item.get("taker_side"),
                timestamp=item.get("created_at"),
            )
            for item in items
        ]
