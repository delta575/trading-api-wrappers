"""Orionx GraphQL public client (Chile, CLP).

Orionx currently requires signed headers even for market data. Unsigned
calls typically fail with HTTP 500 `noContext`. Use :class:`OrionxAuth`
for a working book.
"""

from ..base import Client, ModelMixin
from ..errors import InvalidResponse
from ..market import Market, OrderBook, Ticker, Trade

MARKETS_QUERY = """
query {
  markets {
    code
    name
    mainCurrency { code }
    secondaryCurrency { code }
  }
}
"""

TICKER_QUERY = """
query ticker($code: ID!) {
  market(code: $code) {
    code
    lastTrade { price amount }
  }
}
"""

ORDER_BOOK_QUERY = """
query book($code: ID, $limit: Int) {
  marketOrderBook(marketCode: $code, limit: $limit) {
    buy { limitPrice amount }
    sell { limitPrice amount }
    spread
    mid
  }
}
"""

TRADES_QUERY = """
query trades($code: ID, $limit: Int) {
  market(code: $code) {
    code
    trades(limit: $limit) {
      _id
      amount
      price
      datetime
      type
    }
  }
}
"""


class OrionxPublic(Client, ModelMixin):
    """Orionx GraphQL API without request signing."""

    base_url = "https://api2.orionx.com/"
    error_keys = ["message", "error"]

    def graphql(self, query: str, variables: dict | None = None):
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        return self.post("graphql", json=payload)

    def _decode_response(self, response):
        payload = super()._decode_response(response)
        if isinstance(payload, dict) and payload.get("errors"):
            raise InvalidResponse(str(payload["errors"]), response)
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    def markets(self):
        data = self.graphql(MARKETS_QUERY)
        items = (data or {}).get("markets") or []
        if self.return_json:
            return items
        markets = []
        for item in items:
            main = (item.get("mainCurrency") or {}).get("code")
            quote = (item.get("secondaryCurrency") or {}).get("code")
            markets.append(Market.create(item.get("code"), main, quote, item))
        return markets

    def ticker(self, market_code: str = "BTCCLP"):
        data = self.graphql(TICKER_QUERY, {"code": str(market_code)})
        market = (data or {}).get("market") or {}
        last = (market.get("lastTrade") or {}).get("price")
        if self.return_json:
            return market
        return Ticker.create(market, symbol=str(market_code), last=last)

    def order_book(self, market_code: str = "BTCCLP", limit: int = 25):
        data = self.graphql(
            ORDER_BOOK_QUERY, {"code": str(market_code), "limit": limit}
        )
        book = (data or {}).get("marketOrderBook") or {}
        if self.return_json:
            return book
        return OrderBook.create(
            book, bids=book.get("buy") or [], asks=book.get("sell") or []
        )

    def trades(self, market_code: str = "BTCCLP", limit: int = 20):
        data = self.graphql(TRADES_QUERY, {"code": str(market_code), "limit": limit})
        market = (data or {}).get("market") or {}
        items = market.get("trades") or []
        if self.return_json:
            return items
        return [
            Trade.create(
                item,
                trade_id=item.get("_id"),
                price=item.get("price"),
                amount=item.get("amount"),
                side=item.get("type"),
                timestamp=item.get("datetime"),
            )
            for item in items
        ]
