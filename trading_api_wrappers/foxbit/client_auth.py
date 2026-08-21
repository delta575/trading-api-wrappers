"""Foxbit HMAC-SHA256 authentication."""

from __future__ import annotations

import hashlib
import hmac
import time
from urllib.parse import urlsplit

from requests import PreparedRequest as P

from ..auth import AuthBase
from ..base import AuthMixin
from .client_public import FoxbitPublic


class FoxbitHMACAuth(AuthBase):
    """prehash = timestamp + METHOD + path + query + body."""

    def __init__(self, api_key: str, secret: str):
        self.check_credentials(api_key=api_key, secret=secret)
        self.api_key = api_key
        self.secret = secret

    def __call__(self, r: P):
        timestamp = str(int(time.time() * 1000))
        parts = urlsplit(r.url)
        path = parts.path
        query = f"?{parts.query}" if parts.query else ""
        body = r.body.decode() if isinstance(r.body, bytes) else (r.body or "")
        prehash = f"{timestamp}{r.method.upper()}{path}{query}{body}"
        signature = hmac.new(
            self.secret.encode(), prehash.encode(), hashlib.sha256
        ).hexdigest()
        r.headers["X-FB-ACCESS-KEY"] = self.api_key
        r.headers["X-FB-ACCESS-TIMESTAMP"] = timestamp
        r.headers["X-FB-ACCESS-SIGNATURE"] = signature
        return r


class FoxbitAuth(FoxbitPublic, AuthMixin):
    auth_cls = FoxbitHMACAuth

    def __init__(self, key: str, secret: str, timeout: int | None = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    def balances(self):
        return self.get("accounts")

    def open_orders(self, market_symbol: str | None = None):
        return self.get("orders", params={"market_symbol": market_symbol})

    def new_order(
        self,
        market_symbol: str,
        side: str,
        quantity: float,
        price: float | None = None,
        order_type: str = "LIMIT",
        **kwargs,
    ):
        payload = {
            "market_symbol": str(market_symbol),
            "side": str(side).upper(),
            "type": str(order_type).upper(),
            "quantity": str(quantity),
            "price": str(price) if price is not None else None,
            **kwargs,
        }
        return self.post("orders", json=payload)

    def cancel_order(self, order_id: str, **kwargs):
        payload = {"id": order_id, **kwargs}
        return self.put("orders/cancel", json=payload)

    def order_details(self, order_id: str):
        return self.get(f"orders/by-order-id/{order_id}")

    def order_pages(self, market_symbol: str | None = None, **params):
        return self.get("orders", params={"market_symbol": market_symbol, **params})

    def deposits(self, **params):
        return self.get("deposits", params=params)

    def withdrawals(self, **params):
        return self.get("withdrawals", params=params)

    def withdrawal(self, currency_symbol: str, amount: float, **kwargs):
        payload = {
            "currency_symbol": str(currency_symbol),
            "amount": str(amount),
            **kwargs,
        }
        return self.post("withdrawals", json=payload)

    def deposit_address(self, **params):
        return self.get("deposits/address", params=params)
