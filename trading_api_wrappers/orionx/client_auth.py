"""Orionx HMAC-SHA512 request signing."""

from __future__ import annotations

import hashlib
import hmac
import time

from requests import PreparedRequest as P

from ..auth import AuthBase
from ..base import AuthMixin
from .client_public import OrionxPublic

ME_QUERY = """
query {
  me {
    email
    wallets {
      availableBalance
      currency { code }
    }
  }
}
"""

TRANSFERS_QUERY = """
query {
  me {
    deposits { _id amount status }
    withdrawals { _id amount status }
  }
}
"""

ORDERS_QUERY = """
query orders($onlyOpen: Boolean, $limit: Int) {
  orders(onlyOpen: $onlyOpen, limit: $limit) {
    _id
    amount
    limitPrice
    sell
    status
    type
    market { code }
  }
}
"""

PLACE_LIMIT = """
mutation placeLimit($marketCode: ID, $amount: BigInt, $limitPrice: BigInt, $sell: Boolean) {
  placeLimitOrder(marketCode: $marketCode, amount: $amount, limitPrice: $limitPrice, sell: $sell) {
    _id type amount limitPrice status
  }
}
"""

PLACE_MARKET = """
mutation placeMarket($marketCode: ID, $amount: BigInt, $sell: Boolean) {
  placeMarketOrder(marketCode: $marketCode, amount: $amount, sell: $sell) {
    _id type amount status
  }
}
"""

CANCEL_ORDER = """
mutation cancel($orderId: ID) {
  cancelOrder(orderId: $orderId) { _id status }
}
"""


class OrionxHMACAuth(AuthBase):
    """Sign the raw JSON body: HMAC-SHA512(secret, timestamp + body)."""

    def __init__(self, api_key: str, secret: str):
        self.check_credentials(api_key=api_key, secret=secret)
        self.api_key = api_key
        self.secret = secret

    def __call__(self, r: P):
        body = r.body.decode() if isinstance(r.body, bytes) else (r.body or "")
        timestamp = str(int(time.time()))
        signature = hmac.new(
            self.secret.encode(),
            f"{timestamp}{body}".encode(),
            hashlib.sha512,
        ).hexdigest()
        r.headers["X-ORIONX-TIMESTAMP"] = timestamp
        r.headers["X-ORIONX-APIKEY"] = self.api_key
        r.headers["X-ORIONX-SIGNATURE"] = signature
        r.headers.setdefault("Content-Type", "application/json")
        return r


class OrionxAuth(OrionxPublic, AuthMixin):
    """Signed Orionx client. Required for market data on the live API."""

    auth_cls = OrionxHMACAuth

    def __init__(self, key: str, secret: str, timeout: int | None = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    def me(self):
        return self.graphql(ME_QUERY)

    def balances(self):
        me = (self.me() or {}).get("me") or {}
        return me.get("wallets") or []

    def deposits(self):
        me = (self.graphql(TRANSFERS_QUERY) or {}).get("me") or {}
        return me.get("deposits") or []

    def withdrawals(self):
        me = (self.graphql(TRANSFERS_QUERY) or {}).get("me") or {}
        return me.get("withdrawals") or []

    def order_pages(self, only_open: bool = True, limit: int = 50):
        data = self.graphql(ORDERS_QUERY, {"onlyOpen": only_open, "limit": limit})
        return (data or {}).get("orders") or []

    def open_orders(self, limit: int = 50):
        return self.order_pages(only_open=True, limit=limit)

    def order_details(self, order_id: str):
        for order in self.order_pages(only_open=False, limit=100):
            if str(order.get("_id")) == str(order_id):
                return order
        raise KeyError(order_id)

    def new_order(
        self,
        market_code: str,
        amount: int,
        sell: bool,
        limit_price: int | None = None,
    ):
        if limit_price is None:
            data = self.graphql(
                PLACE_MARKET,
                {"marketCode": market_code, "amount": int(amount), "sell": bool(sell)},
            )
            return (data or {}).get("placeMarketOrder")
        data = self.graphql(
            PLACE_LIMIT,
            {
                "marketCode": market_code,
                "amount": int(amount),
                "limitPrice": int(limit_price),
                "sell": bool(sell),
            },
        )
        return (data or {}).get("placeLimitOrder")

    def cancel_order(self, order_id: str):
        data = self.graphql(CANCEL_ORDER, {"orderId": str(order_id)})
        return (data or {}).get("cancelOrder")
