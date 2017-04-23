import base64
import hashlib
import hmac
import json

# local
from trading_api_wrappers.base import Client, Server
from trading_api_wrappers.common import build_route, check_keys, gen_nonce

from .constants import Path as _p
from . import models as _m
from . import constants as _c

# API server
PROTOCOL = 'https'
HOST = 'www.surbtc.com/api'
TEST_HOST = 'stg.surbtc.com/api'
VERSION = 'v1'

# Limits
ORDERS_LIMIT = 300


class SURBTC(Client):
    Currency = _c.Currency
    Market = _c.Market
    OrderType = _c.OrderType
    OrderState = _c.OrderState
    OrderPriceType = _c.OrderPriceType
    BalanceEvent = _c.BalanceEvent
    QuotationType = _c.QuotationType

    def __init__(self, key=False, secret=False, test=False, timeout=30):
        server = Server(PROTOCOL, HOST if not test else TEST_HOST, VERSION)
        Client.__init__(self, server, timeout)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    # MARKETS------------------------------------------------------------------
    def markets(self):
        url, path = self.url_path_for(_p.MARKETS)
        headers = self._sign_payload(method='GET', path=path)
        data = self.get(url, headers=headers)
        return [_m.Market.create_from_json(market)
                for market in data['markets']]

    def market_details(self, market_id: Market):
        market_id = self.Market.check_param(market_id)
        url, path = self.url_path_for(_p.MARKET_DETAILS,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='GET', path=path)
        data = self.get(url, headers=headers)
        return _m.Market.create_from_json(data['market'])

    def ticker(self, market_id: Market):
        market_id = self.Market.check_param(market_id)
        url, path = self.url_path_for(_p.TICKER,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='GET', path=path)
        data = self.get(url, headers=headers)
        return _m.Ticker.create_from_json(data['ticker'])

    def order_book(self, market_id: Market):
        market_id = self.Market.check_param(market_id)
        url, path = self.url_path_for(_p.ORDER_BOOK,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='GET', path=path)
        data = self.get(url, headers=headers)
        return _m.OrderBook.create_from_json(data['order_book'])

    def quotation(self,
                  market_id: Market,
                  currency: Currency,
                  quotation_type: QuotationType,
                  price_limit: float,
                  amount: float):
        market_id = self.Market.check_param(market_id)
        currency = self.Currency.check_param(currency)
        quotation_type = self.QuotationType.check_param(quotation_type)
        payload = {
            'quotation': {
                'type': quotation_type.value,
                'limit': [str(price_limit), currency.value],
                'amount': [str(amount), currency.value]
            },
        }
        url, path = self.url_path_for(_p.QUOTATION,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='POST', path=path, payload=payload)
        data = self.post(url, headers=headers, data=payload)
        return _m.Quotation.create_from_json(data['quotation'])

    def fee_percentage(self,
                       market_id: Market,
                       order_type: OrderType,
                       market_order: bool = False):
        market_id = self.Market.check_param(market_id)
        order_type = self.OrderType.check_param(order_type)
        params = {
            'type': order_type.value,
            'market_order': market_order,
        }
        url, path = self.url_path_for(_p.FEE_PERCENTAGE,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='GET', path=path, params=params)
        data = self.get(url, headers=headers, params=params)
        return _m.FeePercentage.create_from_json(data['fee_percentage'])

    def trade_transactions(self,
                           market_id: Market,
                           page: int = None,
                           per_page: int = None):
        market_id = self.Market.check_param(market_id)
        params = {
            'page': page,
            'per_page': per_page,
        }
        url, path = self.url_path_for(_p.TRADE_TRANSACTIONS,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='GET', path=path, params=params)
        data = self.get(url, headers=headers, params=params)
        return [_m.TradeTransaction.create_from_json(transaction)
                for transaction in data['trade_transactions']]

    def reports(self,
                market_id,
                report_type,
                from_timestamp=None,
                to_timestamp=None):
        params = {
            'report_type': report_type,
            'from': from_timestamp,
            'to': to_timestamp,
        }
        url, path = self.url_path_for(_p.REPORTS.value, path_arg=market_id)
        headers = self._sign_payload(method='GET', path=path, params=params)
        return self.get(url, headers=headers, params=params)

    # BALANCES-----------------------------------------------------------------
    def balance(self, currency: Currency):
        currency = self.Currency.check_param(currency)
        url, path = self.url_path_for(_p.BALANCES, path_arg=currency.value)
        headers = self._sign_payload(method='GET', path=path)
        data = self.get(url, headers=headers)
        return _m.Balance.create_from_json(data['balance'])

    # Call with 'page' param return authentication error
    def balance_events(self,
                       currencies,
                       event_names,
                       page: int = None,
                       per_page: int = None,
                       relevant: bool = None):
        currencies = [self.Currency.check_param(c).value
                      for c in currencies]
        event_names = [self.BalanceEvent.check_param(e).value
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
        return _m.BalanceEventPages.create_from_json(
            data['balance_events'], data['total_count'], page)

    # ORDERS ------------------------------------------------------------------
    def new_order(self,
                  market_id: Market,
                  order_type: OrderType,
                  price_type: OrderPriceType,
                  amount: float,
                  limit: float = None):
        market_id = self.Market.check_param(market_id)
        order_type = self.OrderType.check_param(order_type)
        price_type = self.OrderPriceType.check_param(price_type)
        payload = {
            'type': order_type.value,
            'price_type': price_type.value,
            'amount': amount,
            'limit': limit,
        }
        return self.new_order_payload(market_id, payload)

    def new_order_payload(self, market_id: Market, payload):
        url, path = self.url_path_for(_p.ORDERS,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='POST', path=path, payload=payload)
        data = self.post(url, headers=headers, data=payload)
        return _m.Order.create_from_json(data['order'])

    def orders(self,
               market_id: Market,
               page: int = None,
               per_page: int = None,
               state: OrderState = None,
               minimum_exchanged: float = None):
        market_id = self.Market.check_param(market_id)
        state = self.OrderState.check_param(state)
        if per_page and per_page > ORDERS_LIMIT:
            msg = f"Param 'per_page' must be <= {ORDERS_LIMIT}"
            raise ValueError(msg)
        params = {
            'per': per_page,
            'page': page,
            'state': state.value if state else state,
            # API has a typo: minimun must be minimum
            'minimun_exchanged': minimum_exchanged,
        }
        url, path = self.url_path_for(_p.ORDERS,
                                      path_arg=market_id.value)
        headers = self._sign_payload(method='GET', path=path, params=params)
        data = self.get(url, headers=headers, params=params)
        return _m.OrderPages.create_from_json(data['orders'], data['meta'])

    def single_order(self, order_id: int):
        url, path = self.url_path_for(_p.SINGLE_ORDER,
                                      path_arg=order_id)
        headers = self._sign_payload(method='GET', path=path)
        data = self.get(url, headers=headers)
        return _m.Order.create_from_json(data['order'])

    def cancel_order(self, order_id: int):
        payload = {
            'state': SURBTC.OrderState.CANCELING.value,
        }
        url, path = self.url_path_for(_p.SINGLE_ORDER,
                                      path_arg=order_id)
        headers = self._sign_payload(method='PUT', path=path, payload=payload)
        data = self.put(url, headers=headers, data=payload)
        return _m.Order.create_from_json(data['order'])

    # PAYMENTS ----------------------------------------------------------------
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
