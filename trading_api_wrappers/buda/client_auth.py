import base64
import hashlib
import hmac
from datetime import datetime

# local
from . import constants as _c
from . import models as _m
from .client_public import BudaPublic
from ..common import build_route, check_keys


class BudaAuth(BudaPublic):

    def __init__(self,
                 key: str=None,
                 secret: str=None,
                 timeout: int=30,
                 host: str=None,
                 return_json: bool=False,
                 retry=None):
        super().__init__(timeout, host, return_json, retry)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    def quotation(self,
                  market_id: str,
                  quotation_type: str,
                  amount: float,
                  limit: float=None):
        data = self.post(f'markets/{market_id}/quotations', data={
            'quotation': {
                'type': str(quotation_type),
                'amount': str(amount),
                'limit': str(limit) if limit else None,
            },
        })
        if self.return_json:
            return data
        return _m.Quotation.create_from_json(data['quotation'])

    def quotation_market(self,
                         market_id: str,
                         quotation_type: str,
                         amount: float):
        return self.quotation(market_id, quotation_type, amount, limit=None)

    def quotation_limit(self,
                        market_id: str,
                        quotation_type: str,
                        amount: float,
                        limit: float):
        return self.quotation(market_id, quotation_type, amount, limit)

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
        data = self.get(f'markets/{market_id}/reports', params={
            'report_type': str(report_type),
            'from': start_at,
            'to': end_at,
        })
        return data

    def report_average_prices(self,
                              market_id: str,
                              start_at: datetime=None,
                              end_at: datetime=None):
        data = self._report(market_id, _c.ReportType.AVERAGE_PRICES,
                            start_at, end_at)
        if self.return_json:
            return data
        return [_m.AveragePrice.create_from_json(report)
                for report in data['reports']]

    def report_candlestick(self,
                           market_id: str,
                           start_at: datetime = None,
                           end_at: datetime = None):
        data = self._report(market_id, _c.ReportType.CANDLESTICK,
                            start_at, end_at)
        if self.return_json:
            return data
        return [_m.Candlestick.create_from_json(report)
                for report in data['reports']]

    # BALANCES-----------------------------------------------------------------
    def balance(self, currency: str):
        data = self.get(f'balances/{currency}')
        if self.return_json:
            return data
        return _m.Balance.create_from_json(data['balance'])

    def balance_event_pages(self,
                            currencies: list,
                            event_names: list,
                            page: int=None,
                            per_page: int=None,
                            relevant: bool=None):
        data = self.get('balance_events', params={
            'currencies[]': [str(c) for c in currencies],
            'event_names[]': [str(e) for e in event_names],
            'page': page,
            'per': per_page,
            'relevant': relevant,
        })
        if self.return_json:
            return data
        # TODO: Response only contains a 'total_count' field instead of meta
        return _m.BalanceEventPages.create_from_json(
            data['balance_events'], data['total_count'], page)

    # ORDERS ------------------------------------------------------------------
    def new_order_payload(self, market_id: str, payload):
        data = self.post(f'markets/{market_id}/orders', payload)
        if self.return_json:
            return data
        return _m.Order.create_from_json(data['order'])

    def new_order(self,
                  market_id: str,
                  order_type: str,
                  price_type: str,
                  amount: float,
                  limit: float=None):
        return self.new_order_payload(market_id, payload={
            'type': str(order_type),
            'price_type': str(price_type),
            'amount': str(amount),
            'limit': str(limit) if limit else None,
        })

    def order_pages(self,
                    market_id: str,
                    page: int=None,
                    per_page: int=None,
                    state: str=None,
                    minimum_exchanged: float=None):
        if per_page and per_page > _c.ORDERS_LIMIT:
            msg = f"Param 'per_page' must be <= {_c.ORDERS_LIMIT}"
            raise ValueError(msg)
        data = self.get(f'markets/{market_id}/orders', params={
            'per': per_page,
            'page': page,
            'state': str(state) if state else None,
            'minimum_exchanged': minimum_exchanged,
        })
        if self.return_json:
            return data
        return _m.OrderPages.create_from_json(data['orders'], data.get('meta'))

    def order_details(self, order_id: int):
        data = self.get(f'orders/{order_id}')
        if self.return_json:
            return data
        return _m.Order.create_from_json(data['order'])

    def cancel_order(self, order_id: int):
        data = self.put(f'orders/{order_id}', data={
            'state': _c.OrderState.CANCELING.value,
        })
        if self.return_json:
            return data
        return _m.Order.create_from_json(data['order'])

    # PAYMENTS ----------------------------------------------------------------
    def _transfers(self, path, model, key):
        data = self.get(path)
        if self.return_json:
            return data
        return [model.create_from_json(transfer)
                for transfer in data[key]]

    def withdrawals(self, currency: str):
        return self._transfers(path=f'currencies/{currency}/withdrawals',
                               model=_m.Withdrawal, key='withdrawals')

    def deposits(self, currency: str):
        return self._transfers(path=f'currencies/{currency}/deposits',
                               model=_m.Deposit, key='deposits')

    # TODO: UNTESTED
    def withdrawal(self,
                   currency: str,
                   amount: float,
                   target_address: str=None,
                   amount_includes_fee: bool=True,
                   simulate: bool=False):
        data = self.post(f'currencies/{currency}/withdrawals', data={
            'withdrawal_data': {
                'target_address': target_address,
            },
            'amount': str(amount),
            'currency': str(currency),
            'simulate': simulate,
            'amount_includes_fee': amount_includes_fee,
        })
        if self.return_json:
            return data
        return _m.Withdrawal.create_from_json(data['withdrawal'])

    def simulate_withdrawal(self,
                            currency: str,
                            amount: float,
                            amount_includes_fee: bool=True):
        return self.withdrawal(
            currency, amount, target_address=None,
            amount_includes_fee=amount_includes_fee, simulate=True)

    # PRIVATE METHODS ---------------------------------------------------------
    def sign(self, method, path, params=None, data=None):
        method = method.upper()
        route = build_route(path, params)
        nonce = self.nonce()

        if data:
            body = data.encode('utf-8')
            encoded_body = base64.standard_b64encode(body).decode('utf-8')
            msg = ' '.join([method, route, encoded_body, nonce])
        else:
            msg = ' '.join([method, route, nonce])

        h = hmac.new(key=self.SECRET.encode('utf-8'),
                     msg=msg.encode('utf-8'),
                     digestmod=hashlib.sha384)

        signature = h.hexdigest()

        return {
            'headers': {
                'X-SBTC-APIKEY': self.KEY,
                'X-SBTC-NONCE': nonce,
                'X-SBTC-SIGNATURE': signature,
                'content-type': 'application/json',
            },
        }
