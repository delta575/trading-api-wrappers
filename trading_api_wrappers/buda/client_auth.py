import base64

from requests import PreparedRequest as P

from . import constants as _c
from . import models as _m
from .client_public import BudaPublic
from ..auth import HMACAuth
from ..base import AuthMixin


class BudaHMACAuth(HMACAuth):

    api_key_header = "X-SBTC-APIKEY"
    nonce_header = "X-SBTC-NONCE"
    signature_header = "X-SBTC-SIGNATURE"
    signature_delimiter = " "
    algorithm = "sha384"

    def build_message(self, r: P, nonce: str):
        components = [r.method, r.path_url]
        if r.body:
            encoded_body = base64.b64encode(r.body).decode()
            components.append(encoded_body)
        components.append(nonce)
        message = self.signature_delimiter.join(components)
        return message


class BudaAuth(BudaPublic, AuthMixin):
    auth_cls = BudaHMACAuth

    def __init__(self, key: str, secret: str, timeout: int = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    # BALANCES-----------------------------------------------------------------
    def balance(self, currency: str):
        data = self.get(f"balances/{currency}")
        if self.return_json:
            return data
        return _m.Balance.create_from_json(data["balance"])

    def balance_event_pages(
        self,
        currencies: list,
        event_names: list,
        page: int = None,
        per_page: int = None,
        relevant: bool = None,
    ):
        data = self.get(
            "balance_events",
            params={
                "currencies[]": [str(c) for c in currencies],
                "event_names[]": [str(e) for e in event_names],
                "page": page,
                "per": per_page,
                "relevant": relevant,
            },
        )
        if self.return_json:
            return data
        # TODO: Response only contains a 'total_count' field instead of meta
        return _m.BalanceEventPages.create_from_json(
            data["balance_events"], data["total_count"], page
        )

    # ORDERS ------------------------------------------------------------------
    def new_order_payload(self, market_id: str, payload):
        data = self.post(f"markets/{market_id}/orders", json=payload)
        if self.return_json:
            return data
        return _m.Order.create_from_json(data["order"])

    def new_order(
        self,
        market_id: str,
        order_type: str,
        price_type: str,
        amount: float,
        limit: float = None,
    ):
        return self.new_order_payload(
            market_id,
            payload={
                "type": str(order_type),
                "price_type": str(price_type),
                "amount": str(amount),
                "limit": str(limit) if limit else None,
            },
        )

    def order_pages(
        self,
        market_id: str,
        page: int = None,
        per_page: int = None,
        state: str = None,
        minimum_exchanged: float = None,
    ):
        if per_page and per_page > _c.ORDERS_LIMIT:
            msg = f"Param 'per_page' must be <= {_c.ORDERS_LIMIT}"
            raise ValueError(msg)
        data = self.get(
            f"markets/{market_id}/orders",
            params={
                "per": per_page,
                "page": page,
                "state": str(state) if state else None,
                "minimum_exchanged": minimum_exchanged,
            },
        )
        if self.return_json:
            return data
        return _m.OrderPages.create_from_json(data["orders"], data.get("meta"))

    def batch_orders(self, cancel_list: list = None, place_list: list = None):
        diff = {"diff": []}
        if cancel_list:
            for idx in cancel_list:
                diff["diff"].append({"mode": "cancel", "order_id": idx})
        if place_list:
            for order in place_list:
                diff["diff"].append({"mode": "place", "order": order})
        data = self.post("orders", json=diff)
        return data

    def order_details(self, order_id: int):
        data = self.get(f"orders/{order_id}")
        if self.return_json:
            return data
        return _m.Order.create_from_json(data["order"])

    def cancel_order(self, order_id: int):
        data = self.put(
            f"orders/{order_id}",
            json={
                "state": _c.OrderState.CANCELING.value,
            },
        )
        if self.return_json:
            return data
        return _m.Order.create_from_json(data["order"])

    # PAYMENTS ----------------------------------------------------------------
    def _transfers(
        self,
        path,
        model,
        key,
        page: int = None,
        per_page: int = None,
        state: str = None,
    ):
        if per_page and per_page > _c.TRANSFERS_LIMIT:
            msg = f"Param 'per_page' must be <= {_c.TRANSFERS_LIMIT}"
            raise ValueError(msg)
        data = self.get(
            path,
            params={
                "per": per_page,
                "page": page,
                "state": str(state) if state else None,
            },
        )
        if self.return_json:
            return data
        return model.create_from_json(data[key], data.get("meta"))

    def withdrawal_pages(self, currency: str, page: int = None, per_page: int = None):
        return self._transfers(
            path=f"currencies/{currency}/withdrawals",
            model=_m.WithdrawalPages,
            key="withdrawals",
            page=page,
            per_page=per_page,
        )

    def withdrawals(self, currency: str, page: int = None, per_page: int = None):
        data = self.withdrawal_pages(currency, page, per_page)
        if isinstance(data, dict):
            return data["withdrawals"]
        return data.withdrawals

    def deposit_pages(self, currency: str, page: int = None, per_page: int = None):
        return self._transfers(
            path=f"currencies/{currency}/deposits",
            model=_m.DepositPages,
            key="deposits",
            page=page,
            per_page=per_page,
        )

    def deposits(self, currency: str, page: int = None, per_page: int = None):
        data = self.deposit_pages(currency, page, per_page)
        if isinstance(data, dict):
            return data["deposits"]
        return data.deposits

    def withdrawal(
        self,
        currency: str,
        amount: float,
        target_address: str = None,
        amount_includes_fee: bool = True,
        simulate: bool = False,
    ):
        data = self.post(
            f"currencies/{currency}/withdrawals",
            json={
                "withdrawal_data": {
                    "target_address": target_address,
                },
                "amount": str(amount),
                "currency": str(currency),
                "simulate": simulate,
                "amount_includes_fee": amount_includes_fee,
            },
        )
        if self.return_json:
            return data
        return _m.Withdrawal.create_from_json(data["withdrawal"])

    def simulate_withdrawal(
        self, currency: str, amount: float, amount_includes_fee: bool = True
    ):
        return self.withdrawal(
            currency,
            amount,
            target_address=None,
            amount_includes_fee=amount_includes_fee,
            simulate=True,
        )
