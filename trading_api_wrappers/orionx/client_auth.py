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
