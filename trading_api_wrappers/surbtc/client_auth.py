import base64
import hashlib
import hmac
import json
from datetime import datetime

# local
from . import constants as _c
from . import models as _m
from ..common import build_route, check_keys, gen_nonce
from .client_public import SURBTCPublic

_p = _c.Path


class SURBTCAuth(SURBTCPublic):

    def __init__(self, key=False, secret=False, test=False, timeout=30):
        SURBTCPublic.__init__(self, test, timeout)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    def quotation(self,
                  market_id: _c.Market,
                  currency: _c.Currency,
                  quotation_type: _c.QuotationType,
                  price_limit: float,
                  amount: float):
        market_id = _c.Market.check(market_id)
        currency = _c.Currency.check(currency)
        quotation_type = _c.QuotationType.check(quotation_type)
        payload = {
            'quotation': {
                'type': quotation_type.value,
                'limit': str([str(price_limit), currency.value]),
                'amount': str([str(amount), currency.value])
            },
        }
        url, path = self.url_path_for(_p.QUOTATION,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='POST', path=path, payload=payload)
        data = self.post(url, headers=headers, data=payload)
        return _m.Quotation.create_from_json(data['quotation'])

    def fee_percentage(self,
                       market_id: _c.Market,
                       order_type: _c.OrderType,
                       market_order: bool=False):
        market_id = _c.Market.check(market_id)
        order_type = _c.OrderType.check(order_type)
        params = {
            'type': order_type.value,
            'market_order': market_order,
        }
        url, path = self.url_path_for(_p.FEE_PERCENTAGE,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='GET', path=path, params=params)
        data = self.get(url, headers=headers, params=params)
        return _m.FeePercentage.create_from_json(data['fee_percentage'])

    def trade_transaction_pages(self,
                                market_id: _c.Market,
                                page: int=None,
                                per_page: int=None):
        market_id = _c.Market.check(market_id)
        # TODO: Pagination isn't working, it always returns 25 items
        params = {
            'page': page,
            'per': per_page,
        }
        url, path = self.url_path_for(_p.TRADE_TRANSACTIONS,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='GET', path=path, params=params)
        data = self.get(url, headers=headers, params=params)
        # TODO: Response doesn't contain a meta field
        return [_m.TradeTransaction.create_from_json(transaction)
                for transaction in data['trade_transactions']]

    # REPORTS -----------------------------------------------------------------
    def report(self,
               market_id: _c.Market,
               report_type: _c.ReportType,
               start_at: datetime=None,
               end_at: datetime=None):
        market_id = _c.Market.check(market_id)
        report_type = _c.ReportType.check(report_type)
        if isinstance(start_at, datetime):
            start_at = int(start_at.timestamp())
        if isinstance(end_at, datetime):
            end_at = int(end_at.timestamp())
        params = {
            'report_type': report_type.value,
            'from': start_at,
            'to': end_at,
        }
        url, path = self.url_path_for(_p.REPORTS,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='GET', path=path, params=params)
        data = self.get(url, headers=headers, params=params)
        # TODO: Report doesn't have a model
        return data

    # BALANCES-----------------------------------------------------------------
    def balance(self, currency: _c.Currency):
        currency = _c.Currency.check(currency)
        url, path = self.url_path_for(_p.BALANCES, path_arg=currency.value)
        headers = self._sign_payload(method='GET', path=path)
        data = self.get(url, headers=headers)
        return _m.Balance.create_from_json(data['balance'])

    def balance_event_pages(self,
                            currencies,
                            event_names,
                            page: int=None,
                            per_page: int=None,
                            relevant: bool=None):
        currencies = [_c.Currency.check(c).value
                      for c in currencies]
        event_names = [_c.BalanceEvent.check(e).value
                       for e in event_names]
        params = {
            'currencies[]': currencies,
            'event_names[]': event_names,
            'page': page,
            'per': per_page,
            'relevant': relevant,
        }
        url, path = self.url_path_for(_p.BALANCES_EVENTS)
        headers = self._sign_payload(method='GET', path=path, params=params)
        data = self.get(url, headers=headers, params=params)
        # TODO: Response only contains a 'total_count' field instead of meta
        return _m.BalanceEventPages.create_from_json(
            data['balance_events'], data['total_count'], page)

    # ORDERS ------------------------------------------------------------------
    def new_order(self,
                  market_id: _c.Market,
                  order_type: _c.OrderType,
                  price_type: _c.OrderPriceType,
                  amount: float,
                  limit: float=None):
        market_id = _c.Market.check(market_id)
        order_type = _c.OrderType.check(order_type)
        price_type = _c.OrderPriceType.check(price_type)
        payload = {
            'type': order_type.value,
            'price_type': price_type.value,
            'amount': str(amount),
            'limit': str(limit),
        }
        return self.new_order_payload(market_id, payload)

    def new_order_payload(self, market_id: _c.Market, payload):
        market_id = _c.Market.check(market_id)
        url, path = self.url_path_for(_p.ORDERS, path_arg=market_id.value)
        headers = self._sign_payload(method='POST', path=path, payload=payload)
        data = self.post(url, headers=headers, data=payload)
        return _m.Order.create_from_json(data['order'])

    def order_pages(self,
                    market_id: _c.Market,
                    page: int=None,
                    per_page: int=None,
                    state: _c.OrderState=None,
                    minimum_exchanged: float=None):
        market_id = _c.Market.check(market_id)
        state = _c.OrderState.check(state)
        if per_page and per_page > _c.ORDERS_LIMIT:
            msg = "Param 'per_page' must be <= {0}".format(_c.ORDERS_LIMIT)
            raise ValueError(msg)
        params = {
            'per': per_page,
            'page': page,
            'state': state.value if state else state,
            'minimum_exchanged': minimum_exchanged,
        }
        url, path = self.url_path_for(_p.ORDERS,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='GET', path=path, params=params)
        data = self.get(url, headers=headers, params=params)
        return _m.OrderPages.create_from_json(data['orders'], data['meta'])

    def order_details(self, order_id: int):
        url, path = self.url_path_for(_p.SINGLE_ORDER,
                                      path_arg=order_id)
        headers = self._sign_payload(method='GET', path=path)
        data = self.get(url, headers=headers)
        return _m.Order.create_from_json(data['order'])

    def cancel_order(self, order_id: int):
        payload = {
            'state': _c.OrderState.CANCELING.value,
        }
        url, path = self.url_path_for(_p.SINGLE_ORDER,
                                      path_arg=order_id)
        headers = self._sign_payload(method='PUT', path=path, payload=payload)
        data = self.put(url, headers=headers, data=payload)
        return _m.Order.create_from_json(data['order'])

    # PAYMENTS ----------------------------------------------------------------
    # TODO: UNTESTED
    def withdraw(self, amount, currency, target_address=None):
        payload = {
            'withdrawal_data': {
                'target_address': target_address,
            },
            'amount': amount,
            'currency': currency,
        }
        url, path = self.url_path_for(_p.WITHDRAWAL, path_arg=currency)
        headers = self._sign_payload(method='POST', path=path, payload=payload)
        return self.post(url, headers=headers, data=payload)

    # PRIVATE METHODS ---------------------------------------------------------
    def _sign_payload(self, method, path, params=None, payload=None):

        route = build_route(path, params)
        nonce = gen_nonce()

        if payload:
            j = json.dumps(payload).encode('utf-8')
            encoded_body = base64.standard_b64encode(j).decode('utf-8')
            string = method + ' ' + route + ' ' + encoded_body + ' ' + nonce
        else:
            string = method + ' ' + route + ' ' + nonce

        h = hmac.new(key=self.SECRET.encode('utf-8'),
                     msg=string.encode('utf-8'),
                     digestmod=hashlib.sha384)

        signature = h.hexdigest()

        return {
            'X-SBTC-APIKEY': self.KEY,
            'X-SBTC-NONCE': nonce,
            'X-SBTC-SIGNATURE': signature,
            'Content-Type': 'application/json',
        }
