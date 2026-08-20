"""Bitso HMAC-SHA256 authentication."""

from __future__ import annotations

import hashlib
import hmac
import time
from urllib.parse import urlsplit

from requests import PreparedRequest as P

from ..auth import AuthBase
from ..base import AuthMixin
from .client_public import BitsoPublic


class BitsoHMACAuth(AuthBase):
    """Authorization: Bitso <key>:<nonce>:<hmac_sha256(nonce+method+path+body)>."""

    def __init__(self, api_key: str, secret: str):
        self.check_credentials(api_key=api_key, secret=secret)
        self.api_key = api_key
        self.secret = secret

    def __call__(self, r: P):
        nonce = str(int(time.time() * 1_000_000))
        path = urlsplit(r.url).path
        query = urlsplit(r.url).query
        request_path = f"{path}?{query}" if query else path
        body = r.body.decode() if isinstance(r.body, bytes) else (r.body or "")
        message = f"{nonce}{r.method}{request_path}{body}"
        signature = hmac.new(
            self.secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        r.headers["Authorization"] = f"Bitso {self.api_key}:{nonce}:{signature}"
        return r


class BitsoAuth(BitsoPublic, AuthMixin):
    auth_cls = BitsoHMACAuth

    def __init__(self, key: str, secret: str, timeout: int | None = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    def balances(self):
        return self.get("balance/")

    def open_orders(self, book: str | None = None):
        return self.get("open_orders/", params={"book": book})

    def new_order(
        self,
        book: str,
        side: str,
        amount: float,
        price: float | None = None,
        order_type: str = "limit",
        **kwargs,
    ):
        payload = {
            "book": str(book),
            "side": str(side).lower(),
            "type": str(order_type).lower(),
            "major": str(amount),
            "price": str(price) if price is not None else None,
            **kwargs,
        }
        return self.post("orders/", json=payload)

    def cancel_order(self, order_id: str):
        return self.delete(f"orders/{order_id}/")

    def order_details(self, order_id: str):
        return self.get(f"orders/{order_id}/")

    def order_pages(self, book: str | None = None, **params):
        return self.get("orders/", params={"book": book, **params})

    def ledger(self, **params):
        return self.get("ledger/", params=params)

    def deposits(self, **params):
        return self.get("fundings/", params=params)

    def withdrawals(self, **params):
        return self.get("withdrawals/", params=params)

    def withdrawal(
        self, currency: str, amount: float, address: str | None = None, **kwargs
    ):
        payload = {
            "currency": str(currency),
            "amount": str(amount),
            "address": address,
            **kwargs,
        }
        return self.post("withdrawals/", json=payload)
