import base64

from requests import PreparedRequest as P

from .client_public_v1 import BitfinexPublic
from ..auth import HMACAuth
from ..base import AuthMixin


class BitfinexHMACAuth(HMACAuth):

    api_key_header = "x-bfx-apikey"
    signature_header = "x-bfx-signature"
    payload_header = "x-bfx-payload"
    algorithm = "sha384"

    def add_nonce(self, r: P, nonce: str):
        pass

    def add_signature(self, r: P, nonce: str):
        message = self.build_message(r, nonce)
        r.headers[self.payload_header] = message
        signature = self.sign(message)
        r.headers[self.signature_header] = signature

    def build_message(self, r: P, nonce: str):
        body = self.load_json(r.body)
        body["request"] = r.path_url
        body["nonce"] = nonce
        encoded_msg = base64.b64encode(self.encode_json(body))
        return encoded_msg


class BitfinexAuth(BitfinexPublic, AuthMixin):
    auth_cls = BitfinexHMACAuth

    def __init__(self, key: str, secret: str, timeout: int = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    # INFO --------------------------------------------------------------------
    # Return information about your account (trading fees).
    def account_info(self):
        return self.get("account_infos")

    # Return information about your account (trading fees).
    def summary(self):
        return self.get("summary")

    # Check the permissions of the key being used to generate this request.
    def key_info(self):
        return self.get("key_info")

    # See your trading wallet information for margin trading.
    def margin_info(self):
        return self.get("margin_infos")

    # See your balances.
    def balances(self):
        return self.get("balances")

    # MOVEMENTS ---------------------------------------------------------------
    # Return your deposit address to make a new deposit.
    def new_deposit(self, method: str, wallet_name: str, renew: bool = None):
        return self.post(
            "deposit/new",
            json={
                "method": method,
                "wallet_name": wallet_name,
                "renew": renew if renew is not None else None,
            },
        )

    # Allow you to move available balances between your wallets.
    def transfer(self, amount: float, currency: str, wallet_from: str, wallet_to: str):
        return self.post(
            "transfer",
            json={
                "amount": str(amount),
                "currency": str(currency),
                "walletfrom": wallet_from,
                "walletto": wallet_to,
            },
        )

    # Allow you to request a withdrawal from one of your wallet.
    def withdraw(self, w_type: str, wallet: str, amount: float, address: str):
        return self.post(
            "withdraw",
            json={
                "withdraw_type": str(w_type),
                "walletselected": wallet,
                "amount": str(amount),
                "address": address,
            },
        )

    # ORDERS ------------------------------------------------------------------
    # Submit a new order.
    def place_order(
        self,
        amount: float,
        price: float,
        side: str,
        ord_type: str,
        symbol: str,
        params: dict = None,
    ):
        payload = {
            "symbol": str(symbol),
            "amount": str(amount),
            "price": str(price),
            "side": str(side),
            "type": str(ord_type),
            "ocoorder": False,
        }
        payload.update(params or {})
        return self.post("order/new", json=payload)

    # Submit a new order.
    def place_oco_order(
        self,
        amount: float,
        price: float,
        side: str,
        ord_type: str,
        symbol: str,
        buy_price_oco: float,
        sell_price_oco: float,
    ):
        return self.place_order(
            amount,
            price,
            side,
            ord_type,
            symbol,
            params={
                "ocoorder": True,
                "buy_price_oco": str(buy_price_oco),
                "sell_price_oco": str(sell_price_oco),
            },
        )

    # Cancel an order.
    def delete_order(self, order_id: int):
        return self.post("order/cancel", json={"order_id": order_id})

    # Cancel all orders.
    def delete_all_order(self):
        return self.post("order/cancel/all")

    # Get the status of an order. Is it active? Was it cancelled?
    # To what extent has it been executed? etc.
    def status_order(self, order_id: int):
        return self.post("order/status", json={"order_id": order_id})

    # View your active orders.
    def active_orders(self):
        return self.post("orders")

    # View your latest inactive orders.
    # Limited to last 3 days and 1 request per minute.
    def orders_history(self, limit: int):
        return self.post("orders/hist", json={"limit": limit})

    # POSITIONS ---------------------------------------------------------------
    # View your active positions.
    def active_positions(self):
        return self.post("positions")

    # Claim a position.
    def claim_position(self, position_id: int):
        return self.post("position/claim", json={"position_id": position_id})

    # HISTORICAL DATA ---------------------------------------------------------
    # View all of your balance ledger entries.
    def balance_history(
        self,
        currency: str,
        since: float = None,
        until: float = None,
        limit: int = None,
        wallet: str = None,
    ):
        return self.post(
            "history",
            json={
                "currency": str(currency),
                "since": since,
                "until": until,
                "limit": limit,
                "wallet": wallet,
            },
        )

    # View your past deposits/withdrawals.
    def movements(
        self,
        currency: str,
        method: str = None,
        since: float = None,
        until: float = None,
        limit: int = None,
    ):
        return self.post(
            "history/movements",
            json={
                "currency": str(currency),
                "method": method,
                "since": since,
                "until": until,
                "limit": limit,
            },
        )

    # View your past trades.
    def past_trades(
        self,
        symbol: str,
        timestamp: float = None,
        until: float = None,
        limit_trades: int = None,
        reverse: bool = None,
    ):
        return self.post(
            "mytrades",
            json={
                "symbol": str(symbol),
                "timestamp": timestamp,
                "until": until,
                "limit_trades": limit_trades,
                "reverse": reverse if reverse is not None else None,
            },
        )

    # MARGIN FUNDING ----------------------------------------------------------
    # Submit a new Offer.
    def place_offer(
        self, currency: str, amount: float, rate: float, period: int, direction: str
    ):
        return self.post(
            "offer/new",
            json={
                "currency": str(currency),
                "amount": str(amount),
                "rate": str(rate),
                "period": period,
                "direction": str(direction),
            },
        )

    # Cancel an offer.
    def cancel_offer(self, offer_id: int):
        return self.post("offer/cancel", json={"offer_id": offer_id})

    # Get the status of an offer. Is it active? Was it cancelled?
    # To what extent has it been executed? etc.
    def status_offer(self, offer_id: int):
        return self.post("offer/status", json={"offer_id": offer_id})

    # View your active offers.
    def active_offers(self):
        return self.post("offers")
