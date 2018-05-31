import hashlib
import hmac
import time

# local
from . import constants as _c
from . import models as _m
from .client_public import CryptoMKTPublic
from ..common import check_keys, clean_parameters


class CryptoMKTAuth(CryptoMKTPublic):

    def __init__(self, key: str=False, secret: str=False, timeout: int=30,
                 return_json=False, retry=None):
        super().__init__(timeout, return_json, retry)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    # BALANCE------------------------------------------------------------------
    def balance(self):
        url, path = self.url_path_for('balance')
        headers = self._sign_payload(path=path)
        data = self.get(url, headers=headers)
        if self.return_json:
            return data
        return _m.Balance.create_from_json(data['data'])

    def wallet_balance(self, currency: str):
        balance = self.balance()
        return getattr(balance, str(currency))

    # ORDERS-------------------------------------------------------------------
    def active_orders(self,
                      market_id: str,
                      page: int=None,
                      limit: int=_c.ORDERS_LIMIT):
        params = {
            'market': str(market_id),
            'page': page,
            'limit': limit,
        }
        url, path = self.url_path_for('orders/active')
        headers = self._sign_payload(path=path)
        data = self.get(url, headers=headers, params=params)
        if self.return_json:
            return data
        return _m.Orders.create_from_json(data['data'], data['pagination'])

    def executed_orders(self,
                        market_id: str,
                        page: int=None,
                        limit: int=_c.ORDERS_LIMIT):
        params = {
            'market': str(market_id),
            'page': page,
            'limit': limit,
        }
        url, path = self.url_path_for('orders/executed')
        headers = self._sign_payload(path=path)
        data = self.get(url, headers=headers, params=params)
        if self.return_json:
            return data
        return _m.Orders.create_from_json(data['data'], data['pagination'])

    def create_order(self,
                     market_id: str,
                     order_type: str,
                     amount: float,
                     price: float):
        payload = {
            'market': str(market_id),
            'type': str(order_type),
            'amount': amount,
            'price': price,
        }
        url, path = self.url_path_for('orders/create')
        headers = self._sign_payload(path=path, payload=payload)
        data = self.post(url, headers=headers, data=payload)
        if self.return_json:
            return data
        return _m.Order.create_from_json(data['data'])

    def order_status(self, order_id: str):
        params = {
            'id': order_id,
        }
        url, path = self.url_path_for('orders/status')
        headers = self._sign_payload(path=path)
        data = self.get(url, headers=headers, params=params)
        if self.return_json:
            return data
        return _m.Order.create_from_json(data['data'])

    def cancel_order(self, order_id: str):
        payload = {
            'id': order_id,
        }
        url, path = self.url_path_for('orders/cancel')
        headers = self._sign_payload(path=path, payload=payload)
        data = self.post(url, headers=headers, data=payload)
        if self.return_json:
            return data
        return _m.Order.create_from_json(data['data'])

    # PAYMENTS-----------------------------------------------------------------
    # TODO: Not tested
    def create_payment(self,
                       amount: float,
                       currency: str,
                       account_email: str,
                       external_id: str=None,
                       callback_url: str=None,
                       error_url: str=None,
                       success_url: str=None,
                       refund_email: str=None):
        payload = {
            'to_receive': amount,
            'to_receive_currency': str(currency),
            'payment_receiver': account_email,
            'external_id': external_id,
            'callback_url': callback_url,
            'error_url': error_url,
            'success_url': success_url,
            'refund_email': refund_email,
        }
        payload = clean_parameters(payload)
        url, path = self.url_path_for('payment/new_order')
        headers = self._sign_payload(path=path, payload=payload)
        data = self.post(url, headers=headers, data=payload)
        if self.return_json:
            return data
        return data

    # TODO: Not tested
    def payment_status(self, payment_id: str):
        params = {
            'id': payment_id,
        }
        url, path = self.url_path_for('payment/status')
        headers = self._sign_payload(path=path)
        data = self.get(url, headers=headers, params=params)
        return data

    # PRIVATE METHODS ---------------------------------------------------------
    def _sign_payload(self, path: str, payload: dict=None):

        timestamp = str(int(time.time()))
        msg = timestamp + path

        if payload:
            for value in [str(payload[k]) for k in sorted(payload.keys())]:
                msg += value

        signature = hmac.new(key=self.SECRET.encode('utf-8'),
                             msg=msg.encode('utf-8'),
                             digestmod=hashlib.sha384).hexdigest()

        # Request fails with 'get_requests_not_allowed' when
        # 'Content-Type': 'application/json' is present
        return {
            'X-MKT-APIKEY': self.KEY,
            'X-MKT-SIGNATURE': signature,
            'X-MKT-TIMESTAMP': timestamp,
        }

    # Request fails with 'get_requests_not_allowed' when
    # json.dumps()' is used
    def _encode_data(self, data):
        return data
