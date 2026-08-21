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
        account_id=None,
        **kwargs,
    ):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret, user_id)
        self.account_id = account_id

    def authenticate(self):
        return self.get("AuthenticateUser")

    def balances(self):
        return self._call("GetAccountPositions")

    def user_accounts(self):
        return self.post("GetUserAccounts", json={})

    def _resolve_account_id(self, account_id=None):
        if account_id is not None:
            return account_id
        if getattr(self, "account_id", None) is not None:
            return self.account_id
        accounts = self.user_accounts()
        if isinstance(accounts, list) and accounts:
            first = accounts[0]
            return first.get("AccountId", first) if isinstance(first, dict) else first
        return None

    def new_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float | None = None,
        order_type: int | None = None,
        account_id=None,
        **kwargs,
    ):
        side_value = 0 if str(side).lower() in {"buy", "bid", "0"} else 1
        otype = 2 if price is not None else 1
        if order_type is not None:
            otype = int(order_type)
        payload = {
            "InstrumentId": self._instrument_id(symbol),
            "AccountId": int(self._resolve_account_id(account_id)),
            "Side": side_value,
            "Quantity": float(quantity),
            "OrderType": otype,
            "TimeInForce": kwargs.pop("time_in_force", 1),
            **kwargs,
        }
        if price is not None:
            payload["LimitPrice"] = float(price)
        return self._call("SendOrder", payload)

    def cancel_order(self, order_id: int, account_id=None, **kwargs):
        return self._call(
            "CancelOrder",
            {
                "OrderId": int(order_id),
                "AccountId": int(self._resolve_account_id(account_id)),
                **kwargs,
            },
        )

    def open_orders(self, account_id=None):
        return self._call(
            "GetOpenOrders",
            {"AccountId": int(self._resolve_account_id(account_id))},
        )

    def order_pages(self, account_id=None, **kwargs):
        return self.open_orders(account_id=account_id)

    def order_details(self, order_id: int, account_id=None):
        return self._call(
            "GetOrderStatus",
            {
                "OrderId": int(order_id),
                "AccountId": int(self._resolve_account_id(account_id)),
            },
        )

    def deposits(self, account_id=None):
        return self._call(
            "GetDepositTickets",
            {"AccountId": int(self._resolve_account_id(account_id))},
        )

    def withdrawals(self, account_id=None):
        return self._call(
            "GetWithdrawTickets",
            {"AccountId": int(self._resolve_account_id(account_id))},
        )

    def withdrawal(self, product_id: int, amount: float, account_id=None, **kwargs):
        return self._call(
            "CreateWithdrawTicket",
            {
                "AccountId": int(self._resolve_account_id(account_id)),
                "ProductId": int(product_id),
                "Amount": float(amount),
                **kwargs,
            },
        )
