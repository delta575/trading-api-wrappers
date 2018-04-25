import base64
import hashlib
import hmac
import json
from datetime import datetime

# local
from . import constants as _c
from . import models as _m
from ..common import build_route, check_keys, gen_nonce
from .client_public import BudaPublic


class BudaAuth(BudaPublic):

    def __init__(self, key: str=False, secret: str=False,
                 timeout: int=30, host: str=None, return_json: bool=False):
        super().__init__(timeout, host, return_json)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    def quotation(self,
                  market_id: str,
                  quotation_type: str,
                  amount: float,
                  limit: float=None):
        payload = {
            'quotation': {
                'type': str(quotation_type),
                'amount': str(amount),
                'limit': str(limit) if limit else None,
            },
        }
        url, path = self.url_path_for('markets/%s/quotations', market_id)
        data = self._sign_and_post(url, path, payload=payload)
        if self.return_json:
            return data
        return _m.Quotation.create_from_json(data['quotation'])

    def quotation_market(self,
                         market_id: str,
                         quotation_type: str,
                         amount: float):
        return self.quotation(
            market_id=market_id, quotation_type=quotation_type,
            amount=amount, limit=None)

    def quotation_limit(self,
                        market_id: str,
                        quotation_type: str,
                        amount: float,
                        limit: float):
        return self.quotation(
            market_id=market_id, quotation_type=quotation_type,
            amount=amount, limit=limit)

    # REPORTS -----------------------------------------------------------------
    def _report(self,
                market_id: str,
                report_type: _c.ReportType,
                start_at: datetime=None,
                end_at: datetime=None):
        if isinstance(start_at, datetime):
            start_at = int(start_at.timestamp())
        if isinstance(end_at, datetime):
            end_at = int(end_at.timestamp())
        params = {
            'report_type': str(report_type),
            'from': start_at,
            'to': end_at,
        }
        url, path = self.url_path_for('markets/%s/reports', market_id)
        data = self._sign_and_get(url, path, params=params)
        return data

    def report_average_prices(self,
                              market_id: str,
                              start_at: datetime=None,
                              end_at: datetime=None):
        data = self._report(
            market_id=market_id, report_type=_c.ReportType.AVERAGE_PRICES,
            start_at=start_at, end_at=end_at)
        if self.return_json:
            return data
        return [_m.AveragePrice.create_from_json(report)
                for report in data['reports']]

    def report_candlestick(self,
                           market_id: str,
                           start_at: datetime = None,
                           end_at: datetime = None):
        data = self._report(
            market_id=market_id, report_type=_c.ReportType.CANDLESTICK,
            start_at=start_at, end_at=end_at)
        if self.return_json:
            return data
        return [_m.Candlestick.create_from_json(report)
                for report in data['reports']]

    # BALANCES-----------------------------------------------------------------
    def balance(self, currency: str):
        url, path = self.url_path_for('balances/%s', currency)
        data = self._sign_and_get(url, path)
        if self.return_json:
            return data
        return _m.Balance.create_from_json(data['balance'])

    def balance_event_pages(self,
                            currencies: list,
                            event_names: list,
                            page: int=None,
                            per_page: int=None,
                            relevant: bool=None):
        currencies = [str(c) for c in currencies]
        event_names = [str(e) for e in event_names]
        params = {
            'currencies[]': currencies,
            'event_names[]': event_names,
            'page': page,
            'per': per_page,
            'relevant': relevant,
        }
        url, path = self.url_path_for('balance_events')
        data = self._sign_and_get(url, path, params=params)
        if self.return_json:
            return data
        # TODO: Response only contains a 'total_count' field instead of meta
        return _m.BalanceEventPages.create_from_json(
            data['balance_events'], data['total_count'], page)

    # ORDERS ------------------------------------------------------------------
    def new_order(self,
                  market_id: str,
                  order_type: str,
                  price_type: str,
                  amount: float,
                  limit: float=None):
        payload = {
            'type': str(order_type),
            'price_type': str(price_type),
            'amount': str(amount),
            'limit': str(limit) if limit else None,
        }
        return self.new_order_payload(market_id, payload)

    def new_order_payload(self, market_id: str, payload):
        url, path = self.url_path_for('markets/%s/orders', market_id)
        data = self._sign_and_post(url, path, payload=payload)
        if self.return_json:
            return data
        return _m.Order.create_from_json(data['order'])

    def order_pages(self,
                    market_id: str,
                    page: int=None,
                    per_page: int=None,
                    state: str=None,
                    minimum_exchanged: float=None):
        if per_page and per_page > _c.ORDERS_LIMIT:
            msg = f"Param 'per_page' must be <= {_c.ORDERS_LIMIT}"
            raise ValueError(msg)
        params = {
            'per': per_page,
            'page': page,
            'state': str(state) if state else None,
            'minimum_exchanged': minimum_exchanged,
        }
        url, path = self.url_path_for('markets/%s/orders', market_id)
        data = self._sign_and_get(url, path, params=params)
        if self.return_json:
            return data
        return _m.OrderPages.create_from_json(data['orders'], data.get('meta'))

    def order_details(self, order_id: int):
        url, path = self.url_path_for('orders/%s', order_id)
        data = self._sign_and_get(url, path)
        if self.return_json:
            return data
        return _m.Order.create_from_json(data['order'])

    def cancel_order(self, order_id: int):
        payload = {
            'state': _c.OrderState.CANCELING.value,
        }
        url, path = self.url_path_for('orders/%s', order_id)
        data = self._sign_and_put(url, path, payload=payload)
        if self.return_json:
            return data
        return _m.Order.create_from_json(data['order'])

    # PAYMENTS ----------------------------------------------------------------
    def _transfers(self, currency: str, path, model, key):
        url, path = self.url_path_for(path, currency)
        data = self._sign_and_get(url, path)
        if self.return_json:
            return data
        return [model.create_from_json(transfer)
                for transfer in data[key]]

    def withdrawals(self, currency: str):
        return self._transfers(currency=currency,
                               path='currencies/%s/withdrawals',
                               model=_m.Withdrawal, key='withdrawals')

    def deposits(self, currency: str):
        return self._transfers(currency=currency,
                               path='currencies/%s/deposits',
                               model=_m.Deposit, key='deposits')

    # TODO: UNTESTED
    def withdrawal(self,
                   currency: str,
                   amount: float,
                   target_address: str=None,
                   amount_includes_fee: bool=True,
                   simulate: bool=False):
        payload = {
            'withdrawal_data': {
                'target_address': target_address,
            },
            'amount': str(amount),
            'currency': str(currency),
            'simulate': simulate,
            'amount_includes_fee': amount_includes_fee,
        }
        url, path = self.url_path_for('currencies/%s/withdrawals', currency)
        data = self._sign_and_post(url, path, payload=payload)
        if self.return_json:
            return data
        return _m.Withdrawal.create_from_json(data['withdrawal'])

    def simulate_withdrawal(self,
                            currency: str,
                            amount: float,
                            amount_includes_fee: bool=True):
        return self.withdrawal(
            currency=currency, amount=amount, target_address=None,
            amount_includes_fee=amount_includes_fee, simulate=True)

    # PRIVATE METHODS ---------------------------------------------------------
    def _sign_payload(self, method, path, params=None, payload=None):

        route = build_route(path, params)
        nonce = gen_nonce()

        if payload:
            j = json.dumps(payload).encode('utf-8')
            encoded_body = base64.standard_b64encode(j).decode('utf-8')
            msg = ' '.join([method, route, encoded_body, nonce])
        else:
            msg = ' '.join([method, route, nonce])

        h = hmac.new(key=self.SECRET.encode('utf-8'),
                     msg=msg.encode('utf-8'),
                     digestmod=hashlib.sha384)

        signature = h.hexdigest()

        return {
            'X-SBTC-APIKEY': self.KEY,
            'X-SBTC-NONCE': nonce,
            'X-SBTC-SIGNATURE': signature,
            'Content-Type': 'application/json',
        }

    def _sign_and_post(self, url, path, params=None, payload=None):
        signed_payload = self._sign_payload('POST', path, params, payload)
        return self.post(url, headers=signed_payload, data=payload)

    def _sign_and_put(self, url, path, params=None, payload=None):
        signed_payload = self._sign_payload('PUT', path, params, payload)
        return self.put(url, headers=signed_payload, data=payload)

    def _sign_and_get(self, url, path, params=None, payload=None):
        signed_payload = self._sign_payload('GET', path, params, payload)
        return self.get(url, headers=signed_payload, params=params)
