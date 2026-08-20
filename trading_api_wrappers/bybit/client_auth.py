"""Bybit HMAC-SHA256 authentication."""

from __future__ import annotations

import hashlib
import hmac
import time
from urllib.parse import urlsplit

from requests import PreparedRequest as P

from ..auth import AuthBase
from ..base import AuthMixin
from .client_public import BybitPublic


class BybitHMACAuth(AuthBase):
    """sign = HMAC-SHA256(secret, timestamp + api_key + recv_window + payload)."""

    recv_window = "5000"

    def __init__(self, api_key: str, secret: str, recv_window: str | None = None):
        self.check_credentials(api_key=api_key, secret=secret)
        self.api_key = api_key
        self.secret = secret
        if recv_window is not None:
            self.recv_window = str(recv_window)

    def __call__(self, r: P):
        timestamp = str(int(time.time() * 1000))
        query = urlsplit(r.url).query
        body = r.body.decode() if isinstance(r.body, bytes) else (r.body or "")
        payload = query or body
        prehash = f"{timestamp}{self.api_key}{self.recv_window}{payload}"
        signature = hmac.new(
            self.secret.encode(), prehash.encode(), hashlib.sha256
        ).hexdigest()
        r.headers["X-BAPI-API-KEY"] = self.api_key
        r.headers["X-BAPI-SIGN"] = signature
        r.headers["X-BAPI-TIMESTAMP"] = timestamp
        r.headers["X-BAPI-RECV-WINDOW"] = self.recv_window
        r.headers["X-BAPI-SIGN-TYPE"] = "2"
        return r


class BybitAuth(BybitPublic, AuthMixin):
    auth_cls = BybitHMACAuth

    def __init__(self, key: str, secret: str, timeout: int | None = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    def balances(self, account_type: str = "UNIFIED"):
        return self.get(
            "account/wallet-balance", params={"accountType": account_type}
        )
