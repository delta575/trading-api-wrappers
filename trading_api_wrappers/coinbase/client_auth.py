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
