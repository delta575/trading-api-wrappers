"""Binance HMAC-SHA256 query signature."""

from __future__ import annotations

import hashlib
import hmac
import time
from urllib.parse import parse_qsl, urlencode

from requests import PreparedRequest as P

from ..auth import AuthBase
from ..base import AuthMixin
from .client_public import BinancePublic


class BinanceHMACAuth(AuthBase):
    """Append timestamp+signature to the query string; header X-MBX-APIKEY."""

    def __init__(self, api_key: str, secret: str):
        self.check_credentials(api_key=api_key, secret=secret)
        self.api_key = api_key
        self.secret = secret

    def __call__(self, r: P):
        url, query = self.url_query_split(r.url)
        params = dict(parse_qsl(query, keep_blank_values=True))
        params.setdefault("timestamp", str(int(time.time() * 1000)))
        total_params = urlencode(params, doseq=True)
        signature = hmac.new(
            self.secret.encode(), total_params.encode(), hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        r.prepare_url(url, params)
        r.headers["X-MBX-APIKEY"] = self.api_key
        return r


class BinanceAuth(BinancePublic, AuthMixin):
    auth_cls = BinanceHMACAuth

    def __init__(self, key: str, secret: str, timeout: int | None = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    def account(self):
        return self.get("account")

    def balances(self):
        return self.account().get("balances")
