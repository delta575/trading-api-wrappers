"""NotBank HMAC authentication (AlphaPoint AuthenticateUser headers)."""

from __future__ import annotations

import hashlib
import hmac
import time

from requests import PreparedRequest as P

from ..auth import AuthBase
from ..base import AuthMixin
from .client_public import NotBankPublic


class NotBankHMACAuth(AuthBase):
    """HMAC-SHA256(secret, nonce + user_id + api_key) on every request."""

    def __init__(self, api_key: str, secret: str, user_id: str | int):
        self.check_credentials(api_key=api_key, secret=secret, user_id=str(user_id))
        self.api_key = api_key
        self.secret = secret
        self.user_id = str(user_id)

    def __call__(self, r: P):
        nonce = str(int(time.time() * 1000))
        message = f"{nonce}{self.user_id}{self.api_key}"
        signature = hmac.new(
            self.secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        r.headers["APIKey"] = self.api_key
        r.headers["UserId"] = self.user_id
        r.headers["Nonce"] = nonce
        r.headers["Signature"] = signature
        return r


class NotBankAuth(NotBankPublic, AuthMixin):
    auth_cls = NotBankHMACAuth

    def __init__(
        self,
        key: str,
        secret: str,
        user_id: str | int,
        timeout: int | None = None,
        **kwargs,
    ):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret, user_id)

    def authenticate(self):
        return self.get("AuthenticateUser")

    def balances(self):
        return self._call("GetAccountPositions")
