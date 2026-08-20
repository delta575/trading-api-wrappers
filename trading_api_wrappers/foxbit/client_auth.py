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
