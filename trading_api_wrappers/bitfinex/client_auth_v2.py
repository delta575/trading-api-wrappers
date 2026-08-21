from urllib.parse import urlsplit

from requests import PreparedRequest as P

from ..auth import HMACAuth
from ..base import AuthMixin
from .client_public_v2 import BitfinexPublic


class BitfinexV2HMACAuth(HMACAuth):
    api_key_header = "bfx-apikey"
    nonce_header = "bfx-nonce"
    signature_header = "bfx-signature"
    algorithm = "sha384"

    def _nonce(self):
        return self.timestamp.milliseconds()

    def build_message(self, r: P, nonce: str):
        path = urlsplit(r.path_url).path
        body = r.body or "{}"
        if isinstance(body, bytes):
            body = body.decode()
        return f"/api{path}{nonce}{body}"


class BitfinexAuth(BitfinexPublic, AuthMixin):
    auth_cls = BitfinexV2HMACAuth

    def __init__(self, key: str, secret: str, timeout: int | None = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    def wallets(self):
        return self.post("auth/r/wallets", json={})

    def orders(self, symbol: str | None = None):
        endpoint = f"auth/r/orders/{symbol}" if symbol else "auth/r/orders"
        return self.post(endpoint, json={})

    def order_history(self, symbol: str):
        return self.post(f"auth/r/orders/{symbol}/hist", json={})

    def user_trades(self, symbol: str):
        return self.post(f"auth/r/trades/{symbol}/hist", json={})

    def balances(self):
        """Alias matching the v1 client."""
        return self.wallets()

    def open_orders(self, symbol: str | None = None):
        return self.orders(symbol)

    def order_pages(self, symbol: str, **params):
        return self.post(f"auth/r/orders/{symbol}/hist", json=params or {})

    def order_details(self, order_id: int, symbol: str | None = None):
        for order in self.orders(symbol) or []:
            oid = order[0] if isinstance(order, (list, tuple)) else order
            if str(oid) == str(order_id):
                return order
        raise KeyError(order_id)

    def new_order(
        self,
        symbol: str,
        amount: float,
        price: float | None = None,
        order_type: str = "EXCHANGE LIMIT",
        **kwargs,
    ):
        payload = {
            "type": order_type,
            "symbol": str(symbol),
            "amount": str(amount),
            "price": str(price) if price is not None else None,
            **kwargs,
        }
        return self.post("auth/w/order/submit", json=payload)

    def cancel_order(self, order_id: int, **kwargs):
        return self.post("auth/w/order/cancel", json={"id": int(order_id), **kwargs})

    def movements(self, currency: str | None = None, **params):
        payload = {"currency": currency, **params}
        return self.post("auth/r/movements/hist", json=payload)

    def deposits(self, currency: str | None = None, **params):
        return self.movements(currency, **params)

    def withdrawals(self, currency: str | None = None, **params):
        return self.movements(currency, **params)

    def withdrawal(
        self,
        wallet: str,
        method: str,
        amount: float,
        address: str,
        **kwargs,
    ):
        return self.post(
            "auth/w/withdraw",
            json={
                "wallet": wallet,
                "method": method,
                "amount": str(amount),
                "address": address,
                **kwargs,
            },
        )
