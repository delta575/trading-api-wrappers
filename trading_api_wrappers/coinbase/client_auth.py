"""Coinbase Exchange HMAC-SHA256 authentication."""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
from urllib.parse import urlsplit

from requests import PreparedRequest as P

from ..auth import AuthBase
from ..base import AuthMixin
from .client_public import CoinbasePublic


class CoinbaseHMACAuth(AuthBase):
    """sign = base64(hmac_sha256(secret, timestamp + method + path + body))."""

    def __init__(self, api_key: str, secret: str, passphrase: str):
        self.check_credentials(api_key=api_key, secret=secret, passphrase=passphrase)
        self.api_key = api_key
        self.secret = secret
        self.passphrase = passphrase

    def __call__(self, r: P):
        timestamp = str(int(time.time()))
        path = urlsplit(r.url).path
        query = urlsplit(r.url).query
        request_path = f"{path}?{query}" if query else path
        body = r.body.decode() if isinstance(r.body, bytes) else (r.body or "")
        prehash = f"{timestamp}{r.method.upper()}{request_path}{body}"
        secret = self.secret
        try:
            key = base64.b64decode(secret)
        except Exception:
            key = secret.encode()
        signature = base64.b64encode(
            hmac.new(key, prehash.encode(), hashlib.sha256).digest()
        ).decode()
        r.headers["CB-ACCESS-KEY"] = self.api_key
        r.headers["CB-ACCESS-SIGN"] = signature
        r.headers["CB-ACCESS-TIMESTAMP"] = timestamp
        r.headers["CB-ACCESS-PASSPHRASE"] = self.passphrase
        return r


class CoinbaseAuth(CoinbasePublic, AuthMixin):
    auth_cls = CoinbaseHMACAuth

    def __init__(
        self,
        key: str,
        secret: str,
        passphrase: str,
        timeout: int | None = None,
        **kwargs,
    ):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret, passphrase)

    def accounts(self):
        return self.get("accounts")

    def balances(self):
        return self.accounts()

    def new_order(
        self,
        product_id: str,
        side: str,
        size: float,
        price: float | None = None,
        order_type: str = "limit",
        **kwargs,
    ):
        payload = {
            "product_id": str(product_id),
            "side": str(side).lower(),
            "size": str(size),
            "type": str(order_type).lower(),
            "price": str(price) if price is not None else None,
            **kwargs,
        }
        return self.post("orders", json=payload)

    def cancel_order(self, order_id: str):
        return self.delete(f"orders/{order_id}")

    def order_details(self, order_id: str):
        return self.get(f"orders/{order_id}")

    def open_orders(self, product_id: str | None = None, **params):
        return self.get(
            "orders",
            params={"product_id": product_id, "status": "open", **params},
        )

    def order_pages(self, product_id: str | None = None, **params):
        return self.get("orders", params={"product_id": product_id, **params})

    def deposits(self, **params):
        return self.get("transfers", params={"type": "deposit", **params})

    def withdrawals(self, **params):
        return self.get("transfers", params={"type": "withdraw", **params})

    def withdrawal(self, currency: str, amount: float, crypto_address: str, **kwargs):
        payload = {
            "currency": currency,
            "amount": str(amount),
            "crypto_address": crypto_address,
            **kwargs,
        }
        return self.post("withdrawals/crypto", json=payload)
