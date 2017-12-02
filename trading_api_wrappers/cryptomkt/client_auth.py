import hashlib
import hmac
import time

# local
from . import constants as _c
from . import models as _m
from ..common import check_keys, clean_parameters
from .client_public import CryptoMKTPublic

_p = _c.Path


class CryptoMKTAuth(CryptoMKTPublic):

    def __init__(self, key=False, secret=False, timeout=30):
        CryptoMKTPublic.__init__(self, timeout)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    # BALANCE------------------------------------------------------------------
    def balance(self):
        url, path = self.url_path_for(_p.BALANCE)
        headers = self._sign_payload(path=path)
        data = self.get(url, headers=headers)
        return _m.Balance.create_from_json(data['data'])

    def wallet_balance(self, currency: _c.Currency):
        currency = _c.Currency.check(currency).value
        balance = self.balance()
        return getattr(balance, currency)

    # ORDERS-------------------------------------------------------------------
    def active_orders(self,
                      market_id: _c.Market,
                      page: int=None,
                      limit: int=_c.ORDERS_LIMIT):
        params = {
            'market': _c.Market.check(market_id).value,
            'page': page,
            'limit': limit,
        }
        url, path = self.url_path_for(_p.ACTIVE_ORDERS)
        headers = self._sign_payload(path=path)
        data = self.get(url, headers=headers, params=params)
        return _m.Orders.create_from_json(data['data'], data['pagination'])

    def executed_orders(self,
                        market_id: _c.Market,
                        page: int=None,
                        limit: int=_c.ORDERS_LIMIT):
        params = {
            'market': _c.Market.check(market_id).value,
            'page': page,
            'limit': limit,
        }
        url, path = self.url_path_for(_p.EXECUTED_ORDERS)
        headers = self._sign_payload(path=path)
        data = self.get(url, headers=headers, params=params)
        return _m.Orders.create_from_json(data['data'], data['pagination'])

    def create_order(self,
                     market_id: _c.Market,
                     order_type: _c.OrderType,
                     amount: float,
                     price: float):
        payload = {
            'market': _c.Market.check(market_id).value,
            'type': _c.OrderType.check(order_type).value,
            'amount': str(amount),
            'price': str(price),
        }
        url, path = self.url_path_for(_p.CREATE_ORDER)
        headers = self._sign_payload(path=path, payload=payload)
        data = self.post(url, headers=headers, data=payload)
        return _m.Order.create_from_json(data['data'])

    def order_status(self, order_id: str):
        params = {
            'id': order_id,
        }
        url, path = self.url_path_for(_p.ORDER_STATUS)
        headers = self._sign_payload(path=path)
        data = self.get(url, headers=headers, params=params)
        return _m.Order.create_from_json(data['data'])

    def cancel_order(self, order_id: str):
        payload = {
            'id': order_id,
        }
        url, path = self.url_path_for(_p.CANCEL_ORDER)
        headers = self._sign_payload(path=path, payload=payload)
        data = self.post(url, headers=headers, data=payload)
        return _m.Order.create_from_json(data['data'])

    # PAYMENTS-----------------------------------------------------------------
    # TODO: Not tested
    def create_payment(self,
                       amount: float,
                       currency: _c.Currency,
                       account_email: str,
                       external_id: str=None,
                       callback_url: str=None,
                       error_url: str=None,
                       success_url: str=None,
                       refund_email: str=None):
        payload = {
            'to_receive': amount,
            'to_receive_currency': _c.Currency.check(currency).value,
            'payment_receiver': account_email,
            'external_id': external_id,
            'callback_url': callback_url,
            'error_url': error_url,
            'success_url': success_url,
            'refund_email': refund_email,
        }
        payload = clean_parameters(payload)
        url, path = self.url_path_for(_p.CREATE_PAYMENT)
        headers = self._sign_payload(path=path, payload=payload)
        data = self.post(url, headers=headers, data=payload)
        return data

    # TODO: Not tested
    def payment_status(self, payment_id: str):
        params = {
            'id': payment_id,
        }
        url, path = self.url_path_for(_p.PAYMENT_STATUS)
        headers = self._sign_payload(path=path)
        data = self.get(url, headers=headers, params=params)
        return data

    # PRIVATE METHODS ---------------------------------------------------------
    def _sign_payload(self, path, payload=None):

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
