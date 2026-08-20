
"""Ripio Trade public REST API (v4) plus retail rates."""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
from urllib.parse import urlsplit

from requests import PreparedRequest as P

from ..auth import AuthBase
from ..base import AuthMixin, Client, ModelMixin
from ..errors import InvalidResponse
from ..market import Trade
from ..trading import BookQuotationMixin
from . import models as _m


class RipioExchangePublic(BookQuotationMixin, Client, ModelMixin):
    """Ripio Trade public REST API (v4)."""

    base_url = "https://api.ripiotrade.co/v4/"
    error_keys = []

    def _decode_response(self, response):
        payload = super()._decode_response(response)
        if isinstance(payload, dict) and "data" in payload:
            if payload.get("error_code"):
                raise InvalidResponse(payload.get("message") or str(payload["error_code"]), response)
            return payload["data"]
        return payload

    def pairs(self):
        return self.get("public/pairs")

    def tickers(self):
        return self.get("public/tickers")

    def ticker(self, pair: str):
        pair = str(pair)
        for item in self.tickers():
            if item.get("pair") == pair:
                return item
        raise KeyError(pair)

    def order_books(self):
        """Return tickers for all pairs (Trade API has no bulk order-book)."""
        return {item["pair"]: item for item in self.tickers()}

    def order_book(self, pair: str, limit: int | None = None):
        data = self.get(
            "public/orders/level-2",
            params={"pair": str(pair), "limit": limit},
        )
        if self.return_json:
            return data
        return _m.OrderBook.create_from_json(data)

    def markets(self):
        return self.pairs()

    def trades(self, pair: str, page_size: int = 50):
        data = self.get(
            "public/trades",
            params={"pair": str(pair), "page_size": page_size},
        )
        items = data.get("trades") if isinstance(data, dict) else data
        if self.return_json:
            return data
        return [
            Trade.create(
                item,
                trade_id=item.get("id"),
                price=item.get("price"),
                amount=item.get("amount"),
                side=item.get("side") or item.get("taker_side"),
                timestamp=item.get("date"),
            )
            for item in items or []
        ]


class RipioPublic(Client, ModelMixin):
    """Ripio retail rates API."""

    base_url = "https://ripio.com/api/v1/"
    error_keys = ["detail"]

    def __init__(self, timeout: int | None = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self._exchange = None
        self._timeout = timeout
        self._kwargs = kwargs

    @property
    def exchange(self):
        if self._exchange is None:
            self._exchange = RipioExchangePublic(self._timeout, **self._kwargs)
        return self._exchange

    def rates_raw(self):
        return self.get("rates/")

    def rates(self):
        data = self.rates_raw()
        data = {"base": data["base"], "rates": data["rates"]}
        if self.return_json:
            return data
        return _m.Rates.create_from_json(data)

    def variation(self):
        data = self.rates_raw()
        return data["variation"]


class RipioHMACAuth(AuthBase):
    """Ripio Trade: HMAC-SHA256(timestamp + method + path + body), base64."""

    def __init__(self, api_key: str, secret: str):
        self.check_credentials(api_key=api_key, secret=secret)
        self.api_key = api_key
        self.secret = secret

    def __call__(self, r: P):
        timestamp = str(int(time.time() * 1000))
        path = urlsplit(r.url).path
        body = r.body.decode() if isinstance(r.body, bytes) else (r.body or "")
        prehash = f"{timestamp}{r.method.upper()}{path}{body}"
        signature = base64.b64encode(
            hmac.new(self.secret.encode(), prehash.encode(), hashlib.sha256).digest()
        ).decode()
        r.headers["Authorization"] = self.api_key
        r.headers["Timestamp"] = timestamp
        r.headers["Signature"] = signature
        return r


class RipioAuth(RipioExchangePublic, AuthMixin):
    """Ripio Trade authenticated client (balances, orders, withdrawals)."""

    auth_cls = RipioHMACAuth

    def __init__(self, key: str, secret: str, timeout: int | None = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    def balances(self, currency_code: str | None = None):
        return self.get("user/balances", params={"currency_code": currency_code})

    def new_order(
        self,
        pair: str,
        side: str,
        amount: float,
        price: float | None = None,
        order_type: str = "limit",
        **kwargs,
    ):
        payload = {
            "pair": str(pair),
            "side": str(side).lower(),
            "type": str(order_type).lower(),
            "amount": amount,
            "price": price,
            **kwargs,
        }
        return self.post("orders", json=payload)

    def cancel_order(self, order_id: str):
        return self.delete("orders", params={"id": order_id})

    def order_details(self, order_id: str):
        return self.get(f"orders/{order_id}")

    def order_pages(self, pair: str | None = None, **params):
        return self.get("orders", params={"pair": pair, **params})

    def open_orders(self, pair: str | None = None):
        return self.get("orders/open", params={"pair": pair})

    def withdrawals(self, **params):
        return self.get("withdrawals", params=params)

    def withdrawal(self, currency_code: str, amount: float, address: str, **kwargs):
        return self.post(
            "withdrawals",
            json={
                "currency_code": currency_code,
                "amount": amount,
                "address": address,
                **kwargs,
            },
        )

    def deposits(self, **params):
        return self.get("deposits", params=params)
