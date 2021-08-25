import json
from urllib.parse import urlsplit

from requests import PreparedRequest as P

from . import constants as _c
from . import models as _m
from .client_public import CryptoMKTPublic
from ..auth import HMACAuth
from ..base import AuthMixin


class CryptoMKTHMACAuth(HMACAuth):

    api_key_header = "X-MKT-APIKEY"
    nonce_header = "X-MKT-TIMESTAMP"
    signature_header = "X-MKT-SIGNATURE"
    signature_delimiter = ""
    algorithm = "sha384"

    def _nonce(self):
        return self.timestamp.seconds()

    def build_message(self, r: P, nonce: str):
        path = urlsplit(r.path_url).path
        body = json.loads(r.body) if r.body else {}
        components = [nonce, path]
        for key in sorted(body.keys()):
            value = str(body[key])
            components.append(value)
        message = self.signature_delimiter.join(components)
        return message


class CryptoMKTAuth(CryptoMKTPublic, AuthMixin):
    auth_cls = CryptoMKTHMACAuth

    def __init__(self, key: str, secret: str, timeout: int = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    # BALANCE------------------------------------------------------------------
    def balance(self):
        data = self.get("balance")
        if self.return_json:
            return data
        return _m.Balance.create_from_json(data["data"])

    def wallet_balance(self, currency: str):
        balance = self.balance()
        return getattr(balance, str(currency))

    # ORDERS-------------------------------------------------------------------
    def active_orders(
        self, market_id: str, page: int = None, limit: int = _c.ORDERS_LIMIT
    ):
        data = self.get(
            "orders/active",
            params={
                "market": str(market_id),
                "page": page,
                "limit": limit,
            },
        )
        if self.return_json:
            return data
        return _m.Orders.create_from_json(data["data"], data["pagination"])

    def executed_orders(
        self, market_id: str, page: int = None, limit: int = _c.ORDERS_LIMIT
    ):
        data = self.get(
            "orders/executed",
            params={
                "market": str(market_id),
                "page": page,
                "limit": limit,
            },
        )
        if self.return_json:
            return data
        return _m.Orders.create_from_json(data["data"], data["pagination"])

    def create_order(
        self, market_id: str, order_type: str, amount: float, price: float
    ):
        data = self.post(
            "orders/create",
            json={
                "market": str(market_id),
                "type": str(order_type),
                "amount": amount,
                "price": price,
            },
        )
        if self.return_json:
            return data
        return _m.Order.create_from_json(data["data"])

    def order_status(self, order_id: str):
        data = self.get(
            "orders/status",
            params={
                "id": order_id,
            },
        )
        if self.return_json:
            return data
        return _m.Order.create_from_json(data["data"])

    def cancel_order(self, order_id: str):
        data = self.get(
            "orders/cancel",
            params={
                "id": order_id,
            },
        )
        if self.return_json:
            return data
        return _m.Order.create_from_json(data["data"])

    # PAYMENTS-----------------------------------------------------------------
    # TODO: Not tested
    def create_payment(
        self,
        amount: float,
        currency: str,
        account_email: str,
        external_id: str = None,
        callback_url: str = None,
        error_url: str = None,
        success_url: str = None,
        refund_email: str = None,
    ):
        data = self.post(
            "payment/new_order",
            json={
                "to_receive": amount,
                "to_receive_currency": str(currency),
                "payment_receiver": account_email,
                "external_id": external_id,
                "callback_url": callback_url,
                "error_url": error_url,
                "success_url": success_url,
                "refund_email": refund_email,
            },
        )
        if self.return_json:
            return data
        return data

    # TODO: Not tested
    def payment_status(self, payment_id: str):
        data = self.get(
            "payment/status",
            params={
                "id": payment_id,
            },
        )
        return data
