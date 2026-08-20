"""OKX HMAC-SHA256 (base64) authentication."""

from __future__ import annotations

import base64
import hashlib
import hmac
from datetime import datetime, timezone
from urllib.parse import urlsplit

from requests import PreparedRequest as P

from ..auth import AuthBase
from ..base import AuthMixin
from .client_public import OKXPublic


class OKXHMACAuth(AuthBase):
    """sign = base64(hmac_sha256(secret, timestamp + method + path + body))."""

    def __init__(self, api_key: str, secret: str, passphrase: str):
        self.check_credentials(api_key=api_key, secret=secret, passphrase=passphrase)
        self.api_key = api_key
        self.secret = secret
        self.passphrase = passphrase

    def __call__(self, r: P):
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        path = urlsplit(r.url).path
        query = urlsplit(r.url).query
        request_path = f"{path}?{query}" if query else path
        body = r.body.decode() if isinstance(r.body, bytes) else (r.body or "")
        prehash = f"{timestamp}{r.method.upper()}{request_path}{body}"
        signature = base64.b64encode(
            hmac.new(self.secret.encode(), prehash.encode(), hashlib.sha256).digest()
        ).decode()
        r.headers["OK-ACCESS-KEY"] = self.api_key
        r.headers["OK-ACCESS-SIGN"] = signature
        r.headers["OK-ACCESS-TIMESTAMP"] = timestamp
        r.headers["OK-ACCESS-PASSPHRASE"] = self.passphrase
        return r


class OKXAuth(OKXPublic, AuthMixin):
    auth_cls = OKXHMACAuth

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

    def balances(self):
        return self.get("account/balance")
