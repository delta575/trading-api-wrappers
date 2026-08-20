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

    def new_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float | None = None,
        order_type: str = "LIMIT",
        **kwargs,
    ):
        params = {
            "symbol": str(symbol),
            "side": str(side).upper(),
            "type": str(order_type).upper(),
            "quantity": quantity,
            "price": price,
            **kwargs,
        }
        return self.post("order", params=params)

    def cancel_order(self, symbol: str, order_id: int | None = None, **kwargs):
        params = {"symbol": str(symbol), "orderId": order_id, **kwargs}
        return self.delete("order", params=params)

    def order_details(self, symbol: str, order_id: int | None = None, **kwargs):
        params = {"symbol": str(symbol), "orderId": order_id, **kwargs}
        return self.get("order", params=params)

    def open_orders(self, symbol: str | None = None):
        return self.get("openOrders", params={"symbol": symbol})

    def order_pages(self, symbol: str, **params):
        return self.get("allOrders", params={"symbol": str(symbol), **params})

    def deposits(self, coin: str | None = None, **params):
        return self.get(
            "/sapi/v1/capital/deposit/hisrec",
            params={"coin": coin, **params},
        )

    def withdrawals(self, coin: str | None = None, **params):
        return self.get(
            "/sapi/v1/capital/withdraw/history",
            params={"coin": coin, **params},
        )

    def withdrawal(self, coin: str, address: str, amount: float, **kwargs):
        return self.post(
            "/sapi/v1/capital/withdraw/apply",
            params={"coin": coin, "address": address, "amount": amount, **kwargs},
        )
