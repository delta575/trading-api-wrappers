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

    def new_order(
        self,
        inst_id: str,
        side: str,
        sz: float,
        px: float | None = None,
        ord_type: str = "limit",
        td_mode: str = "cash",
        **kwargs,
    ):
        payload = {
            "instId": str(inst_id),
            "tdMode": td_mode,
            "side": str(side).lower(),
            "ordType": str(ord_type).lower(),
            "sz": str(sz),
            "px": str(px) if px is not None else None,
            **kwargs,
        }
        return self.post("trade/order", json=payload)

    def cancel_order(self, inst_id: str, ord_id: str | None = None, **kwargs):
        payload = {"instId": str(inst_id), "ordId": ord_id, **kwargs}
        return self.post("trade/cancel-order", json=payload)

    def order_details(self, inst_id: str, ord_id: str | None = None, **kwargs):
        return self.get(
            "trade/order",
            params={"instId": str(inst_id), "ordId": ord_id, **kwargs},
        )

    def open_orders(self, inst_type: str = "SPOT", inst_id: str | None = None):
        return self.get(
            "trade/orders-pending",
            params={"instType": inst_type, "instId": inst_id},
        )

    def order_pages(self, inst_type: str = "SPOT", **params):
        return self.get(
            "trade/orders-history",
            params={"instType": inst_type, **params},
        )

    def deposits(self, **params):
        return self.get("asset/deposit-history", params=params)

    def withdrawals(self, **params):
        return self.get("asset/withdrawal-history", params=params)

    def withdrawal(self, ccy: str, amt: float, to_addr: str, **kwargs):
        payload = {"ccy": ccy, "amt": str(amt), "toAddr": to_addr, **kwargs}
        return self.post("asset/withdrawal", json=payload)
