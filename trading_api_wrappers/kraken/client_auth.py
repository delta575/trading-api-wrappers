import base64
import hashlib
import hmac
from urllib.parse import urlencode

# local
from . import constants as _c
from ..common import check_keys, clean_parameters, gen_nonce
from .client_public import KrakenPublic

_p = _c.Path


class KrakenAuth(KrakenPublic):

    def __init__(self, key=False, secret=False, timeout=30):
        KrakenPublic.__init__(self, timeout)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    # Private user data -------------------------------------------------------
    # Get account balance.
    def balance(self):
        url, path = self.url_path_for(_p.BALANCE)
        payload = {
            'nonce': 0
        }
        return self._sign_and_post(url, path, payload)

    # Get trade balance.
    def trade_balance(self, asset=_c.Currency.ZUSD.value,
                      asset_class='currency'):
        payload = {
            'asset': asset,
            'aclass': asset_class,
        }
        url, path = self.url_path_for(_p.TRADE_BALANCE)
        return self._sign_and_post(url, path, payload)

    # Get open orders.
    def open_orders(self, include_trades=False, userref=None):
        payload = {
            'trades': include_trades,
            'userref': userref,
        }
        url, path = self.url_path_for(_p.OPEN_ORDERS)
        return self._sign_and_post(url, path, payload)

    # Get closed orders.
    def closed_orders(self, include_trades=False, userref=None, start=None,
                      end=None, ofs=None, closetime='both'):
        payload = {
            'trades': include_trades,
            'userref': userref,
            'start': start,
            'end': end,
            'ofs': ofs,
            'closetime': closetime,
        }
        url, path = self.url_path_for(_p.CLOSED_ORDERS)
        return self._sign_and_post(url, path, payload)

    # Query orders info.
    def query_orders(self, txid=None, include_trades=False, userref=None):
        payload = {
            'trades': include_trades,
            'userref': userref,
            'txid': txid,
        }
        url, path = self.url_path_for(_p.QUERY_ORDERS)
        return self._sign_and_post(url, path, payload)

    # Get trades history.
    def trades_history(self, trade_type='all', include_trades=False,
                       start=None, end=None, ofs=None):
        payload = {
            'type': trade_type,
            'trades': include_trades,
            'start': start,
            'end': end,
            'ofs': ofs,
        }
        url, path = self.url_path_for(_p.TRADES_HISTORY)
        return self._sign_and_post(url, path, payload)

    # Query trades info.
    def query_trades(self, txid, include_trades=False):
        payload = {
            'txid': txid,
            'trades': include_trades,
        }
        url, path = self.url_path_for(_p.QUERY_TRADES)
        return self._sign_and_post(url, path, payload)

    # Query trades info.
    def open_positions(self, txid=None, include_pl=False):
        payload = {
            'txid': txid,
            'docalcs': include_pl,
        }
        url, path = self.url_path_for(_p.OPEN_POSITIONS)
        return self._sign_and_post(url, path, payload)

    # Get ledgers info.
    def ledgers(self, asset_class='currency', asset='all', ledger_type='all',
                start=None, end=None, ofs=None):
        payload = {
            'aclass': asset_class,
            'asset': asset,
            'type': ledger_type,
            'start': start,
            'end': end,
            'ofs': ofs,
        }
        url, path = self.url_path_for(_p.LEDGERS)
        return self._sign_and_post(url, path, payload)

    # Query ledgers.
    def query_ledgers(self, ledger_id):
        payload = {
            'id': ledger_id,
        }
        url, path = self.url_path_for(_p.QUERY_LEDGERS)
        return self._sign_and_post(url, path, payload)

    # Get trade volume.
    def trade_volume(self, pair=None, fee_info=None):
        payload = {
            'pair': pair,
            'fee-info': fee_info,
        }
        url, path = self.url_path_for(_p.TRADE_VOLUME)
        return self._sign_and_post(url, path, payload)

    # Private user trading  ---------------------------------------------------
    # Add standard order
    def add_order(self, pair, direction, order_type, price, volume,
                  price2=None, leverage=None, oflags=None, starttm=0,
                  expiretm=0, userref=None, validate=None, c_ordertype=None,
                  c_price=None, c_price2=None):
        payload = {
            'pair': pair,
            'type': direction,
            'ordertype': order_type,
            'price': price,
            'price2': price2,
            'volume': volume,
            'leverage': leverage,
            'oflags': oflags,
            'starttm': starttm,
            'expiretm': expiretm,
            'userref': userref,
            'validate': validate,
            'close[ordertype]': c_ordertype,
            'close[price]': c_price,
            'close[price2]': c_price2,
        }
        url, path = self.url_path_for(_p.ADD_ORDER)
        return self._sign_and_post(url, path, payload)

    # Cancel open order
    def cancel_order(self, txid):
        payload = {
            'txid': txid,
        }
        url, path = self.url_path_for(_p.CANCEL_ORDER)
        return self._sign_and_post(url, path, payload)

    # Private user funding  ---------------------------------------------------
    # Get deposit methods.
    def deposit_methods(self, asset, asset_class='currency'):
        payload = {
            'aclass': asset_class,
            'asset': asset,
        }
        url, path = self.url_path_for(_p.DEPOSIT_METHODS)
        return self._sign_and_post(url, path, payload)

    # Get deposit addresses
    def deposit_addresses(self, asset, method, asset_class='currency',
                          new=False):
        payload = {
            'aclass': asset_class,
            'asset': asset,
            'method': method,
            'new': new,
        }
        url, path = self.url_path_for(_p.DEPOSIT_ADDRESSES)
        return self._sign_and_post(url, path, payload)

    # Get status of recent deposits
    def deposit_status(self, asset, method, asset_class='currency'):
        payload = {
            'aclass': asset_class,
            'asset': asset,
            'method': method,
        }
        url, path = self.url_path_for(_p.DEPOSIT_STATUS)
        return self._sign_and_post(url, path, payload)

    # Get withdrawal information
    def withdraw_info(self, asset, amount, key, asset_class='currency'):
        payload = {
            'aclass': asset_class,
            'asset': asset,
            'amount': amount,
            'key': key,
        }
        url, path = self.url_path_for(_p.WITHDRAW_INFO)
        return self._sign_and_post(url, path, payload)

    # Withdraw funds
    def withdraw(self, asset, amount, key, asset_class='currency'):
        payload = {
            'aclass': asset_class,
            'asset': asset,
            'amount': amount,
            'key': key,
        }
        url, path = self.url_path_for(_p.WITHDRAW)
        return self._sign_and_post(url, path, payload)

    # Get status of recent withdrawals
    def withdraw_status(self, asset, method, asset_class='currency'):
        payload = {
            'aclass': asset_class,
            'asset': asset,
            'method': method,
        }
        url, path = self.url_path_for(_p.WITHDRAW_STATUS)
        return self._sign_and_post(url, path, payload)

    # Request withdrawal cancellation
    def withdraw_cancel(self, asset, refid, asset_class='currency'):
        payload = {
            'aclass': asset_class,
            'asset': asset,
            'refid': refid,
        }
        url, path = self.url_path_for(_p.WITHDRAW_CANCEL)
        return self._sign_and_post(url, path, payload)

    # PRIVATE METHODS ---------------------------------------------------------
    def _sign_payload(self, path, data=None):
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
            'API-Sign': sig_digest.decode()
        }

    def _encode_data(self, data):
        encoded_data = urlencode(data) if data else data
        return encoded_data

    # Packs and sign the payload and send the request with POST.
    def _sign_and_post(self, url, path, payload):
        payload = clean_parameters(payload)
        signed_payload = self._sign_payload(path, payload)
        return self.post(url, headers=signed_payload, data=payload)
