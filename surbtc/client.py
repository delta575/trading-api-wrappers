from urllib.parse import urlparse, urlencode
import json
import base64
import hmac
import hashlib
import time
# pip
import requests

# API server
PROTOCOL = 'https'
HOST = 'www.surbtc.com/api'
TEST_HOST = 'stg.surbtc.com/api'
VERSION = 'v1'

# API paths
PATH_MARKETS = 'markets'
PATH_MARKET_DETAILS = 'markets/%s'
PATH_INDICATORS = "markets/%s/indicators"
PATH_ORDER_BOOK = 'markets/%s/order_book'
PATH_QUOTATION = 'markets/%s/quotations'
PATH_FEE_PERCENTAGE = 'markets/%s/fee_percentage'
PATH_TRADE_TRANSACTIONS = 'markets/%s/trade_transactions'
PATH_REPORTS = 'markets/%s/reports'
PATH_BALANCES = 'balances/%s'
PATH_BALANCES_EVENTS = 'balance_events'
PATH_ORDERS = 'markets/%s/orders'
PATH_SINGLE_ORDER = 'orders/%s'
PATH_WITHDRAWAL = 'withdrawals'


class SURBTC(object):

    def __init__(self, key=False, secret=False, test=False, timeout=30):

        # Check for keys
        if not key or not secret:
            raise ValueError("Api Key and Secret are needed!")

        self.KEY = str(key)
        self.SECRET = str(secret)

        self.URL = '{0:s}://{1:s}/{2:s}'.format(PROTOCOL, HOST if not test else TEST_HOST, VERSION)
        self.TIMEOUT = timeout

    @property
    def _nonce(self):
        time.sleep(0.2)
        return str(int((time.time() * 1000)))

    # MARKETS-----------------------------------------------------------------------------------------------------------
    
    def markets(self):
        url, path = self._url_path_for(PATH_MARKETS)
        signed_payload = self._sign_payload(method='GET', path=path)
        return self._get(url, headers=signed_payload)

    def market_details(self, market_id):
        url, path = self._url_path_for(PATH_MARKET_DETAILS, path_arg=market_id)
        signed_payload = self._sign_payload(method='GET', path=path)
        return self._get(url, headers=signed_payload)

    def indicators(self, market_id):
        url, path = self._url_path_for(PATH_INDICATORS, path_arg=market_id)
        signed_payload = self._sign_payload(method='GET', path=path)
        return self._get(url, headers=signed_payload)

    def order_book(self, market_id):
        url, path = self._url_path_for(PATH_ORDER_BOOK, path_arg=market_id)
        signed_payload = self._sign_payload(method='GET', path=path)
        return self._get(url, headers=signed_payload)

    def quotation(self, market_id, quotation_type, reverse, amount):
        payload = {
            'quotation': {
                'type': quotation_type,
                'reverse': reverse,
                'amount': str(amount),
            },
        }
        url, path = self._url_path_for(PATH_QUOTATION, path_arg=market_id)
        signed_payload = self._sign_payload(method='POST', path=path, payload=payload)
        return self._post(url, headers=signed_payload, data=payload)

    def fee_percentage(self, market_id, order_type, market_order=False):
        parameters = {
            'type': order_type,
            'market_order': market_order,
        }
        url, path = self._url_path_for(PATH_FEE_PERCENTAGE, path_arg=market_id)
        signed_payload = self._sign_payload(method='GET', path=path, params=parameters)
        return self._get(url, headers=signed_payload, params=parameters)

    def trade_transactions(self, market_id, page=None, per_page=None):
        parameters = {
            'page': page,
            'per_page': per_page,
        }
        url, path = self._url_path_for(PATH_TRADE_TRANSACTIONS, path_arg=market_id)
        signed_payload = self._sign_payload(method='GET', path=path, params=parameters)
        return self._get(url, headers=signed_payload, params=parameters)

    def reports(self, market_id, report_type, from_timestamp=None, to_timestamp=None):
        parameters = {
            'report_type': report_type,
            'from': from_timestamp,
            'to': to_timestamp,
        }
        url, path = self._url_path_for(PATH_REPORTS, path_arg=market_id)
        signed_payload = self._sign_payload(method='GET', path=path, params=parameters)
        return self._get(url, headers=signed_payload, params=parameters)

    # BALANCES----------------------------------------------------------------------------------------------------------
    
    def balance(self, currency):
        url, path = self._url_path_for(PATH_BALANCES, path_arg=currency)
        signed_payload = self._sign_payload(method='GET', path=path)
        return self._get(url, headers=signed_payload)

    # Call with 'page' param return authentication error
    def balance_events(self, currencies, event_names, page=None, per_page=None, relevant=True):
        parameters = {
            'currencies[]': currencies,
            'event_names[]': event_names,
            'page': page,
            'per': per_page,
            'relevant': relevant,
        }
        url, path = self._url_path_for(PATH_BALANCES_EVENTS)
        signed_payload = self._sign_payload(method='GET', path=path, params=parameters)
        return self._get(url, headers=signed_payload, params=parameters)

    # ORDERS------------------------------------------------------------------------------------------------------------
    
    def new_order(self, market_id, order_type, limit, amount, original_amount, price_type):
        payload = {
            'type': order_type,
            'limit': limit,
            'amount': amount,
            'original_amount': original_amount,
            'price_type': price_type,
        }
        return self.new_order_payload(market_id, payload)

    def new_order_payload(self, market, payload):
        url, path = self._url_path_for(PATH_ORDERS, path_arg=market)
        signed_payload = self._sign_payload(method='POST', path=path, payload=payload)
        return self._post(url, headers=signed_payload, data=payload)

    def orders(self, market_id, page=None, per_page=None, state=None):
        parameters = {
            'per': per_page,
            'page': page,
            'state': state,
        }
        url, path = self._url_path_for(PATH_ORDERS, path_arg=market_id)
        signed_payload = self._sign_payload(method='GET', path=path, params=parameters)
        return self._get(url, headers=signed_payload, params=parameters)

    def single_order(self, order_id):
        url, path = self._url_path_for(PATH_SINGLE_ORDER, path_arg=order_id)
        signed_payload = self._sign_payload(method='GET', path=path)
        return self._get(url, headers=signed_payload)

    def cancel_order(self, order_id):
        payload = {
            'state': 'canceling',
        }
        url, path = self._url_path_for(PATH_SINGLE_ORDER, path_arg=order_id)
        signed_payload = self._sign_payload(method='PUT', path=path, payload=payload)
        return self._put(url, headers=signed_payload, data=payload)

    # PAYMENTS----------------------------------------------------------------------------------------------------------
    
    def withdraw(self, target_address, amount, currency='BTC'):
        payload = {
            'withdrawal_data': {
                'target_address': target_address,
            },
            'amount': str(amount),
            'currency': currency,
        }
        url, path = self._url_path_for(PATH_WITHDRAWAL)
        signed_payload = self._sign_payload(method='POST', path=path, payload=payload)
        return self._post(url, headers=signed_payload, data=payload)

    # PRIVATE METHODS---------------------------------------------------------------------------------------------------
    
    def _get(self, url, headers, params=None):
        response = requests.get(url, headers=headers, params=params, verify=True, timeout=self.TIMEOUT)
        json_resp = response.json()
        self._check_response(json_resp)
        return json_resp

    def _put(self, url, headers, data):
        response = requests.put(url, headers=headers, data=json.dumps(data), verify=True, timeout=self.TIMEOUT)
        json_resp = response.json()
        self._check_response(json_resp)
        return json_resp

    def _post(self, url, headers, data):
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=True, timeout=self.TIMEOUT)
        json_resp = response.json()
        self._check_response(json_resp)
        return json_resp

    def _url_path_for(self, path, path_arg=None):
        url = '{0:s}/{1:s}'.format(self.URL, path)

        if path_arg:
            url = url % path_arg

        return url, urlparse(url).path

    def _check_response(self, response):
        if 'message' in response:
            raise Exception(response['message'])

    def _build_parameters(self, parameters):
        if parameters:
            p = {k: v for k, v in parameters.items() if v is not None}
            return urlencode(p, True)
        else:
            return None

    def _build_route(self, path, params=None):
        built_params = self._build_parameters(params)
        if built_params:
            return '{0:s}?{1:s}'.format(path, built_params)
        else:
            return path

    def _sign_payload(self, method, path, params=None, payload=None):

        route = self._build_route(path, params)
        nonce = self._nonce

        if payload:
            j = json.dumps(payload).encode('utf-8')
            encoded_body = base64.standard_b64encode(j).decode('utf-8')
            string_to_sign = method + ' ' + route + ' ' + encoded_body + ' ' + nonce
        else:
            string_to_sign = method + ' ' + route + ' ' + nonce

        h = hmac.new(self.SECRET.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha384)
        signature = h.hexdigest()

        return {
            'X-SBTC-APIKEY': self.KEY,
            'X-SBTC-NONCE': nonce,
            'X-SBTC-SIGNATURE': signature,
            'Content-Type': 'application/json'
        }
