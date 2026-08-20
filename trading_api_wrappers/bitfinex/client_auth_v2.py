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
