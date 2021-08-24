import base64
import hashlib
import hmac

from requests import PreparedRequest as P

from .client_public import KrakenPublic
from ..auth import HMACAuth
from ..base import AuthMixin


class KrakenHMACAuth(HMACAuth):

    api_key_header = "API-Key"
    signature_header = "API-Sign"
    algorithm = "sha512"

    def add_nonce(self, r: P, nonce: str):
        body = self.parse_data(r.body)
        body["nonce"] = nonce
        r.prepare_body(data=body, files=None)

    def build_message(self, r: P, nonce: str):
        auth = (nonce + r.body).encode()
        digest = hashlib.sha256(auth).digest()
        message = r.path_url.encode() + digest
        return message

    def sign(self, msg: str):

        h = hmac.new(
            key=base64.b64decode(self.secret), msg=msg, digestmod=self.algorithm
        )

        signature = base64.b64encode(h.digest()).decode()

        return signature


class KrakenAuth(KrakenPublic, AuthMixin):
    auth_cls = KrakenHMACAuth

    def __init__(self, key: str, secret: str, timeout: int = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.add_auth(key, secret)

    # Private user data -------------------------------------------------------
    # Get account balance.
    def balance(self):
        return self.post("private/Balance")

    # Get trade balance.
    def trade_balance(self, asset: str = None, asset_class: str = None):
        return self.post(
            "private/TradeBalance",
            data={
                "asset": str(asset) if asset else None,
                "aclass": str(asset_class) if asset_class else None,
            },
        )

    # Get open orders.
    def open_orders(self, include_trades: bool = None, userref: str = None):
        return self.post(
            "private/OpenOrders",
            data={
                "trades": include_trades,
                "userref": userref,
            },
        )

    # Get closed orders.
    def closed_orders(
        self,
        include_trades: bool = None,
        userref: str = None,
        start: int = None,
        end: int = None,
        ofs: int = None,
        closetime: int = None,
    ):
        return self.post(
            "private/ClosedOrders",
            data={
                "trades": include_trades,
                "userref": userref,
                "start": start,
                "end": end,
                "ofs": ofs,
                "closetime": closetime,
            },
        )

    # Query orders info.
    def query_orders(
        self, txid: list, include_trades: bool = None, userref: str = None
    ):
        return self.post(
            "private/QueryOrders",
            data={
                "txid": txid,
                "trades": include_trades,
                "userref": userref,
            },
        )

    # Get trades history.
    def trades_history(
        self,
        trade_type: str = None,
        include_trades: bool = None,
        start: int = None,
        end: int = None,
        ofs: int = None,
    ):
        return self.post(
            "private/TradesHistory",
            data={
                "type": str(trade_type) if trade_type else None,
                "trades": include_trades,
                "start": start,
                "end": end,
                "ofs": ofs,
            },
        )

    # Query trades info.
    def query_trades(self, txid: list, include_trades: bool = None):
        return self.post(
            "private/QueryTrades",
            data={
                "txid": txid,
                "trades": include_trades,
            },
        )

    # Query trades info.
    def open_positions(self, txid: list = None, include_pl: bool = None):
        return self.post(
            "private/OpenPositions",
            data={
                "txid": txid,
                "docalcs": include_pl,
            },
        )

    # Get ledgers info.
    def ledgers(
        self,
        asset_class: str = None,
        asset: str = None,
        ledger_type: str = None,
        start: int = None,
        end: int = None,
        ofs: int = None,
    ):
        return self.post(
            "private/Ledgers",
            data={
                "aclass": str(asset_class) if asset_class else None,
                "asset": str(asset) if asset else None,
                "type": str(ledger_type) if ledger_type else None,
                "start": start,
                "end": end,
                "ofs": ofs,
            },
        )

    # Query ledgers.
    def query_ledgers(self, ledger_id: str):
        return self.post(
            "private/QueryLedgers",
            data={
                "id": ledger_id,
            },
        )

    # Get trade volume.
    def trade_volume(self, pair: str = None, fee_info: bool = None):
        return self.post(
            "private/TradeVolume",
            data={
                "pair": str(pair) if pair else None,
                "fee-info": fee_info,
            },
        )

    # Private user trading  ---------------------------------------------------
    # Add standard order
    def add_order(
        self,
        pair: str,
        direction: str,
        order_type: str,
        volume: float,
        price: float = None,
        price2: float = None,
        leverage: float = None,
        oflags: list = None,
        starttm: int = None,
        expiretm: int = None,
        userref: str = None,
        validate: bool = None,
        c_ordertype: str = None,
        c_price: float = None,
        c_price2: float = None,
    ):
        return self.post(
            "private/AddOrder",
            data={
                "pair": str(pair),
                "type": str(direction),
                "ordertype": str(order_type),
                "price": price,
                "price2": price2,
                "volume": volume,
                "leverage": leverage,
                "oflags": oflags,
                "starttm": starttm,
                "expiretm": expiretm,
                "userref": userref,
                "validate": validate,
                "close[ordertype]": str(c_ordertype) if c_ordertype else None,
                "close[price]": c_price,
                "close[price2]": c_price2,
            },
        )

    # Cancel open order
    def cancel_order(self, txid: str):
        return self.post(
            "private/CancelOrder",
            data={
                "txid": txid,
            },
        )

    # Private user funding  ---------------------------------------------------
    # Get deposit methods.
    def deposit_methods(self, asset: str, asset_class: str = None):
        return self.post(
            "private/DepositMethods",
            data={
                "asset": str(asset),
                "aclass": str(asset_class) if asset_class else None,
            },
        )

    # Get deposit addresses
    def deposit_addresses(
        self, asset: str, method: str, asset_class: str = None, new: bool = None
    ):
        return self.post(
            "private/DepositAddresses",
            data={
                "asset": str(asset),
                "method": str(method),
                "aclass": str(asset_class) if asset_class else None,
                "new": new,
            },
        )

    # Get status of recent deposits
    def deposit_status(self, asset: str, method: str, asset_class: str = None):
        return self.post(
            "private/DepositStatus",
            data={
                "asset": str(asset),
                "method": str(method),
                "aclass": str(asset_class) if asset_class else None,
            },
        )

    # Get withdrawal information
    def withdraw_info(
        self, asset: str, amount: float, key: str, asset_class: str = None
    ):
        return self.post(
            "private/WithdrawInfo",
            data={
                "asset": str(asset),
                "aclass": str(asset_class) if asset_class else None,
                "amount": amount,
                "key": key,
            },
        )

    # Withdraw funds
    def withdraw(self, asset: str, amount: float, key: str, asset_class: str = None):
        return self.post(
            "private/Withdraw",
            data={
                "asset": str(asset),
                "aclass": str(asset_class) if asset_class else None,
                "amount": amount,
                "key": key,
            },
        )

    # Get status of recent withdrawals
    def withdraw_status(self, asset: str, method: str, asset_class: str = None):
        return self.post(
            "private/WithdrawStatus",
            data={
                "asset": str(asset),
                "method": str(method),
                "aclass": str(asset_class) if asset_class else None,
            },
        )

    # Request withdrawal cancellation
    def withdraw_cancel(self, asset: str, refid: str, asset_class: str = None):
        return self.post(
            "private/WithdrawCancel",
            data={
                "asset": str(asset),
                "aclass": str(asset_class) if asset_class else None,
                "refid": refid,
            },
        )
