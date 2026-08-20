"""Mercado Bitcoin Trade API (TAPI) v3 authentication."""

from __future__ import annotations

import hashlib
import hmac
import time
from urllib.parse import urlsplit

from requests import PreparedRequest as P

from ..auth import AuthBase
from ..base import AuthMixin, Client, ModelMixin
from ..errors import InvalidResponse


class MercadoBitcoinTAPIAuth(AuthBase):
    """TAPI-MAC = HMAC-SHA512(secret, path + '?' + body)."""

    def __init__(self, tapi_id: str, tapi_secret: str):
        self.check_credentials(tapi_id=tapi_id, tapi_secret=tapi_secret)
        self.tapi_id = tapi_id
        self.tapi_secret = tapi_secret

    def __call__(self, r: P):
        path = urlsplit(r.url).path
        if not path.endswith("/"):
            path = f"{path}/"
        body = r.body.decode() if isinstance(r.body, bytes) else (r.body or "")
        message = f"{path}?{body}"
        mac = hmac.new(
            self.tapi_secret.encode(), message.encode(), hashlib.sha512
        ).hexdigest()
        r.headers["TAPI-ID"] = self.tapi_id
        r.headers["TAPI-MAC"] = mac
        return r


class MercadoBitcoinAuth(Client, AuthMixin, ModelMixin):
    """Authenticated TAPI client (balances / orders)."""

    base_url = "https://www.mercadobitcoin.net/tapi/v3/"
    error_keys = ["error_message", "message"]
    auth_cls = MercadoBitcoinTAPIAuth

    def __init__(
        self,
        tapi_id: str,
        tapi_secret: str,
        timeout: int | None = None,
        **kwargs,
    ):
        super().__init__(timeout, **kwargs)
        self.add_auth(tapi_id, tapi_secret)

    def _decode_response(self, response):
        payload = super()._decode_response(response)
        if isinstance(payload, dict) and payload.get("status") not in (None, 100):
            raise InvalidResponse(
                payload.get("error_message") or str(payload.get("status")),
                response,
            )
        if isinstance(payload, dict) and "response_data" in payload:
            return payload["response_data"]
        return payload

    def _tapi(self, method: str, **params):
        payload = {
            "tapi_method": method,
            "tapi_nonce": int(time.time() * 1000),
            **params,
        }
        return self.post("", data=payload)

    def balances(self):
        return self._tapi("get_account_info")

    def list_orders(self, coin_pair: str, **params):
        return self._tapi("list_orders", coin_pair=str(coin_pair), **params)
