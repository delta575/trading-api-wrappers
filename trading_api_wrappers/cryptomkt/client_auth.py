import hashlib
import hmac

# local
from . import constants as _c
from . import models as _m
from .client_public import CryptoMKTPublic
from ..common import check_keys, clean_parameters


class CryptoMKTAuth(CryptoMKTPublic):

    def __init__(self,
                 key: str=None,
                 secret: str=None,
                 timeout: int=30,
                 return_json=False,
                 retry=None):
        super().__init__(timeout, return_json, retry)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    # BALANCE------------------------------------------------------------------
    def balance(self):
        data = self.get('balance')
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
        data = self.get('orders/active', params={
            'market': str(market_id),
            'page': page,
            'limit': limit,
        })
        if self.return_json:
            return data
        return _m.Orders.create_from_json(data['data'], data['pagination'])

    def executed_orders(self,
                        market_id: str,
                        page: int=None,
                        limit: int=_c.ORDERS_LIMIT):
        data = self.get('orders/executed', params={
            'market': str(market_id),
            'page': page,
            'limit': limit,
        })
        if self.return_json:
            return data
        return _m.Orders.create_from_json(data['data'], data['pagination'])

    def create_order(self,
                     market_id: str,
                     order_type: str,
                     amount: float,
                     price: float):
        data = self.post('orders/create', data={
            'market': str(market_id),
            'type': str(order_type),
            'amount': amount,
            'price': price,
        })
        if self.return_json:
            return data
        return _m.Order.create_from_json(data['data'])

    def order_status(self, order_id: str):
        data = self.get('orders/status', params={
            'id': order_id,
        })
        if self.return_json:
            return data
        return _m.Order.create_from_json(data['data'])

    def cancel_order(self, order_id: str):
        data = self.get('orders/cancel', params={
            'id': order_id,
        })
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
        data = self.post('payment/new_order', data={
            'to_receive': amount,
            'to_receive_currency': str(currency),
            'payment_receiver': account_email,
            'external_id': external_id,
            'callback_url': callback_url,
            'error_url': error_url,
            'success_url': success_url,
            'refund_email': refund_email,
        })
        if self.return_json:
            return data
        return data

    # TODO: Not tested
    def payment_status(self, payment_id: str):
        data = self.get('payment/status', params={
            'id': payment_id,
        })
        return data

    # PRIVATE METHODS ---------------------------------------------------------
    def sign(self, method, path, params=None, data=None):
        timestamp = str(self.seconds())
        msg = timestamp + path

        if data:
            for value in [str(data[k]) for k in sorted(data.keys())]:
                msg += value

        h = hmac.new(key=self.SECRET.encode('utf-8'),
                     msg=msg.encode('utf-8'),
                     digestmod=hashlib.sha384)

        signature = h.hexdigest()

        # Request fails with 'get_requests_not_allowed' when
        # 'Content-Type': 'application/json' is present
        return {
            'headers': {
                'X-MKT-APIKEY': self.KEY,
                'X-MKT-SIGNATURE': signature,
                'X-MKT-TIMESTAMP': timestamp,
            },
        }

    # Request fails with 'get_requests_not_allowed' when
    # json.dumps()' is used
    def _encode_data(self, data):
        return clean_parameters(data or {})
