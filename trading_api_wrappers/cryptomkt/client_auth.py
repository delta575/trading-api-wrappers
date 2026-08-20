from __future__ import annotations

import hashlib
import hmac
import time
from base64 import b64encode
from urllib.parse import urlsplit

from requests import PreparedRequest as P

from ..auth import AuthBase
from ..base import AuthMixin
from . import models as _m
from .client_public import CryptoMKTPublic


class CryptoMKTHS256Auth(AuthBase):
    """CryptoMarket API v3 HS256 authentication."""

    def __init__(self, api_key: str, secret: str, window: int | None = None):
        self.api_key = api_key
        self.secret = secret
        self.window = window

    def __call__(self, r: P):
        url = urlsplit(r.url)
        parts = [r.method, url.path]
        if url.query:
            parts.extend(["?", url.query])
        if r.body:
            body = r.body.decode() if isinstance(r.body, bytes) else r.body
            parts.append(body)
        timestamp = str(int(time.time() * 1000))
        parts.append(timestamp)
        if self.window is not None:
            parts.append(str(self.window))
        signature = hmac.new(
            self.secret.encode(), "".join(parts).encode(), hashlib.sha256
        ).hexdigest()
        payload = [self.api_key, signature, timestamp]
        if self.window is not None:
            payload.append(str(self.window))
        token = b64encode(":".join(payload).encode()).decode()
        r.headers["Authorization"] = f"HS256 {token}"
        return r


class CryptoMKTAuth(CryptoMKTPublic, AuthMixin):
    auth_cls = CryptoMKTHS256Auth

    def __init__(self, key: str, secret: str, timeout: int | None = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    def balance(self, currency: str | None = None):
        endpoint = f"spot/balance/{currency}" if currency else "spot/balance"
        data = self.get(endpoint)
        if self.return_json:
            return data
        if currency:
            return _m.WalletBalance.create_from_json({"currency": str(currency), **data})
        return [_m.WalletBalance.create_from_json(item) for item in data]

    def wallet_balance(self, currency: str):
        return self.balance(currency)

    def active_orders(self, symbol: str | None = None):
        data = self.get("spot/order", params={"symbol": str(symbol) if symbol else None})
        if self.return_json:
            return data
        return [_m.Order.create_from_json(order) for order in data]

    def executed_orders(self, symbol: str | None = None, limit: int | None = None):
        data = self.get(
            "spot/history/order",
            params={
                "symbol": str(symbol) if symbol else None,
                "limit": limit,
            },
        )
        if self.return_json:
            return data
        return [_m.Order.create_from_json(order) for order in data]

    def order_status(self, client_order_id: str):
        data = self.get(f"spot/order/{client_order_id}")
        if self.return_json:
            return data
        return _m.Order.create_from_json(data)

    def create_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float | None = None,
        order_type: str = "limit",
    ):
        payload = {
            "symbol": str(symbol),
            "side": str(side),
            "quantity": str(quantity),
            "type": str(order_type),
        }
        if price is not None:
            payload["price"] = str(price)
        data = self.post("spot/order", data=payload)
        if self.return_json:
            return data
        return _m.Order.create_from_json(data)

    def cancel_order(self, client_order_id: str):
        data = self.delete(f"spot/order/{client_order_id}")
        if self.return_json:
            return data
        return _m.Order.create_from_json(data)
