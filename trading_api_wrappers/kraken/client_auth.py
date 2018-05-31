import base64
import hashlib
import hmac
from urllib.parse import urlencode

# local
from .client_public import KrakenPublic
from ..common import check_keys, clean_parameters, gen_nonce


class KrakenAuth(KrakenPublic):

    def __init__(self, key: str=False, secret: str=False, timeout: int=30,
                 retry=None):
        super().__init__(timeout, retry)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    # Private user data -------------------------------------------------------
    # Get account balance.
    def balance(self):
        url, path = self.url_path_for('private/Balance')
        return self._sign_and_post(url, path, payload={})

    # Get trade balance.
    def trade_balance(self,
                      asset: str=None,
                      asset_class: str=None):
        payload = {
            'asset': str(asset) if asset else None,
            'aclass': str(asset_class) if asset_class else None,
        }
        url, path = self.url_path_for('private/TradeBalance')
        return self._sign_and_post(url, path, payload)

    # Get open orders.
    def open_orders(self,
                    include_trades: bool=None,
                    userref: str=None):
        payload = {
            'trades': include_trades,
            'userref': userref,
        }
        url, path = self.url_path_for('private/OpenOrders')
        return self._sign_and_post(url, path, payload)

    # Get closed orders.
    def closed_orders(self,
                      include_trades: bool=None,
                      userref: str=None,
                      start: int=None,
                      end: int=None,
                      ofs: int=None,
                      closetime: int=None):
        payload = {
            'trades': include_trades,
            'userref': userref,
            'start': start,
            'end': end,
            'ofs': ofs,
            'closetime': closetime,
        }
        url, path = self.url_path_for('private/ClosedOrders')
        return self._sign_and_post(url, path, payload)

    # Query orders info.
    def query_orders(self,
                     txid: list,
                     include_trades: bool=None,
                     userref: str=None):
        payload = {
            'txid': txid,
            'trades': include_trades,
            'userref': userref,
        }
        url, path = self.url_path_for('private/QueryOrders')
        return self._sign_and_post(url, path, payload)

    # Get trades history.
    def trades_history(self,
                       trade_type: str=None,
                       include_trades: bool=None,
                       start: int=None,
                       end: int=None,
                       ofs: int=None):
        payload = {
            'type': str(trade_type) if trade_type else None,
            'trades': include_trades,
            'start': start,
            'end': end,
            'ofs': ofs,
        }
        url, path = self.url_path_for('private/TradesHistory')
        return self._sign_and_post(url, path, payload)

    # Query trades info.
    def query_trades(self,
                     txid: list,
                     include_trades: bool=None):
        payload = {
            'txid': txid,
            'trades': include_trades,
        }
        url, path = self.url_path_for('private/QueryTrades')
        return self._sign_and_post(url, path, payload)

    # Query trades info.
    def open_positions(self,
                       txid: list=None,
                       include_pl: bool=None):
        payload = {
            'txid': txid,
            'docalcs': include_pl,
        }
        url, path = self.url_path_for('private/OpenPositions')
        return self._sign_and_post(url, path, payload)

    # Get ledgers info.
    def ledgers(self,
                asset_class: str=None,
                asset: str=None,
                ledger_type: str=None,
                start: int=None,
                end: int=None,
                ofs: int=None):
        payload = {
            'aclass': str(asset_class) if asset_class else None,
            'asset': str(asset) if asset else None,
            'type': str(ledger_type) if ledger_type else None,
            'start': start,
            'end': end,
            'ofs': ofs,
        }
        url, path = self.url_path_for('private/Ledgers')
        return self._sign_and_post(url, path, payload)

    # Query ledgers.
    def query_ledgers(self, ledger_id: str):
        payload = {
            'id': ledger_id,
        }
        url, path = self.url_path_for('private/QueryLedgers')
        return self._sign_and_post(url, path, payload)

    # Get trade volume.
    def trade_volume(self,
                     pair: str=None,
                     fee_info: bool=None):
        payload = {
            'pair': str(pair) if pair else None,
            'fee-info': fee_info,
        }
        url, path = self.url_path_for('private/TradeVolume')
        return self._sign_and_post(url, path, payload)

    # Private user trading  ---------------------------------------------------
    # Add standard order
    def add_order(self,
                  pair: str,
                  direction: str,
                  order_type: str,
                  volume: float,
                  price: float=None,
                  price2: float=None,
                  leverage: float=None,
                  oflags: list=None,
                  starttm: int=None,
                  expiretm: int=None,
                  userref: str=None,
                  validate: bool=None,
                  c_ordertype: str=None,
                  c_price: float=None,
                  c_price2: float=None):
        payload = {
            'pair': str(pair),
            'type': str(direction),
            'ordertype': str(order_type),
            'price': price,
            'price2': price2,
            'volume': volume,
            'leverage': leverage,
            'oflags': oflags,
            'starttm': starttm,
            'expiretm': expiretm,
            'userref': userref,
            'validate': validate,
            'close[ordertype]': str(c_ordertype) if order_type else None,
            'close[price]': c_price,
            'close[price2]': c_price2,
        }
        url, path = self.url_path_for('private/AddOrder')
        return self._sign_and_post(url, path, payload)

    # Cancel open order
    def cancel_order(self, txid: str):
        payload = {
            'txid': txid,
        }
        url, path = self.url_path_for('private/CancelOrder')
        return self._sign_and_post(url, path, payload)

    # Private user funding  ---------------------------------------------------
    # Get deposit methods.
    def deposit_methods(self,
                        asset: str,
                        asset_class: str=None):
        payload = {
            'asset': str(asset),
            'aclass': str(asset_class) if asset_class else None,
        }
        url, path = self.url_path_for('private/DepositMethods')
        return self._sign_and_post(url, path, payload)

    # Get deposit addresses
    def deposit_addresses(self,
                          asset: str,
                          method: str,
                          asset_class: str=None,
                          new: bool=None):
        payload = {
            'asset': str(asset),
            'method': str(method),
            'aclass': str(asset_class) if asset_class else None,
            'new': new,
        }
        url, path = self.url_path_for('private/DepositAddresses')
        return self._sign_and_post(url, path, payload)

    # Get status of recent deposits
    def deposit_status(self,
                       asset: str,
                       method: str,
                       asset_class: str=None):
        payload = {
            'asset': str(asset),
            'method': str(method),
            'aclass': str(asset_class) if asset_class else None,
        }
        url, path = self.url_path_for('private/DepositStatus')
        return self._sign_and_post(url, path, payload)

    # Get withdrawal information
    def withdraw_info(self,
                      asset: str,
                      amount: float,
                      key: str,
                      asset_class: str=None):
        payload = {
            'asset': str(asset),
            'aclass': str(asset_class) if asset_class else None,
            'amount': amount,
            'key': key,
        }
        url, path = self.url_path_for('private/WithdrawInfo')
        return self._sign_and_post(url, path, payload)

    # Withdraw funds
    def withdraw(self,
                 asset: str,
                 amount: float,
                 key: str,
                 asset_class: str=None):
        payload = {
            'asset': str(asset),
            'aclass': str(asset_class) if asset_class else None,
            'amount': amount,
            'key': key,
        }
        url, path = self.url_path_for('private/Withdraw')
        return self._sign_and_post(url, path, payload)

    # Get status of recent withdrawals
    def withdraw_status(self,
                        asset: str,
                        method: str,
                        asset_class: str=None):
        payload = {
            'asset': str(asset),
            'method': str(method),
            'aclass': str(asset_class) if asset_class else None,
        }
        url, path = self.url_path_for('private/WithdrawStatus')
        return self._sign_and_post(url, path, payload)

    # Request withdrawal cancellation
    def withdraw_cancel(self,
                        asset: str,
                        refid: str,
                        asset_class: str=None):
        payload = {
            'asset': str(asset),
            'aclass': str(asset_class) if asset_class else None,
            'refid': refid,
        }
        url, path = self.url_path_for('private/WithdrawCancel')
        return self._sign_and_post(url, path, payload)

    # PRIVATE METHODS ---------------------------------------------------------
    def _sign_payload(self, path: str, data: dict=None):
        data['nonce'] = gen_nonce()
        encoded_data = self._encode_data(data)

        # Unicode-objects must be encoded before hashing
        encoded = (str(data['nonce']) + encoded_data).encode()
        message = path.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(key=base64.b64decode(self.SECRET),
                             msg=message,
                             digestmod=hashlib.sha512)
        sig_digest = base64.b64encode(signature.digest())

        return {
            'API-Key': self.KEY,
            'API-Sign': sig_digest.decode(),
        }

    def _encode_data(self, data):
        encoded_data = urlencode(data) if data else data
        return encoded_data

    # Packs and sign the payload and send the request with POST.
    def _sign_and_post(self, url: str, path: str, payload: dict):
        payload = clean_parameters(payload)
        signed_payload = self._sign_payload(path, payload)
        return self.post(url, headers=signed_payload, data=payload)
