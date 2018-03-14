import json
from enum import Enum
from urllib.parse import urlparse

# pip
import requests

# local
from . import errors


class Server(object):

    def __init__(self, protocol, host, version=None):
        url = f'{protocol}://{host}'
        if version:
            url = f'{url}/{version}'

        self.PROTOCOL = protocol
        self.HOST = host
        self.VERSION = version
        self.URL = url


class Client(object):

    error_key = ''

    def __init__(self, server: Server, timeout=30):
        self.SERVER = server
        self.TIMEOUT = timeout

    def get(self, url, headers=None, params=None):
        response = self._request('get', url, headers=headers, params=params)
        return response

    def put(self, url, headers, data):
        response = self._request('put', url, headers=headers, data=data)
        return response

    def post(self, url, headers, data):
        response = self._request('post', url, headers=headers, data=data)
        return response

    def _request(self, method, url, headers, params=None, data=None):
        data = self._encode_data(data)
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data,
            verify=True,
            timeout=self.TIMEOUT)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise errors.InvalidResponse(response) from e
        json_resp = self._resp_to_json(response)
        return json_resp

    def _encode_data(self, data):
        data = json.dumps(data) if data else data
        return data

    def _resp_to_json(self, response):
        try:
            json_resp = response.json()
        except json.decoder.JSONDecodeError as e:
            raise errors.DecodeError() from e
        if isinstance(json_resp, dict):
            if bool(json_resp.get(self.error_key, False)):
                raise errors.InvalidResponse(response)
        return json_resp

    def url_for(self, path, path_arg=None):
        url = f'{self.SERVER.URL}/{path}'
        if path_arg:
            url = url % path_arg
        return url

    def url_path_for(self, path, path_arg=None):
        url = self.url_for(path, path_arg)
        path = urlparse(url).path
        return url, path


class StandardClient(object):
    def __init__(self):
        pass

    @staticmethod
    def get_quote(orderbook, quote_max_accumulated):
        results = []
        for operation_type in ('bids', 'asks'):
            quoted_accumulated = 0
            base_accumulated = 0
            for entry in orderbook[operation_type]:
                quote_expent = entry[0] * entry[1]
                if quote_max_accumulated > quoted_accumulated + quote_expent:
                    quoted_accumulated += quote_expent
                    base_accumulated += entry[0]
                else:
                    remaining_quote = quote_max_accumulated - quoted_accumulated
                    quoted_accumulated += remaining_quote
                    base_accumulated += remaining_quote/entry[1]
                    break
            if quoted_accumulated != quote_max_accumulated:
                results.append(None)
            else:
                results.append(quoted_accumulated/base_accumulated)
        return results

    @staticmethod
    def base_standarize_orderbook(raw_orderbook, get_row):
        orderbook = {}
        orderbook['bids'] = sorted(
            [[float(entry_el) for entry_el in get_row(entry)] for entry in raw_orderbook['bids']],
            key=lambda x: x[1], reverse=True
        )
        orderbook['asks'] = sorted(
            [[float(entry_el) for entry_el in get_row(entry)] for entry in raw_orderbook['asks']],
            key=lambda x: x[1], reverse=False
        )
        return orderbook


class _Enum(Enum):
    @staticmethod
    def _format_value(value):
        return str(value).upper()

    @classmethod
    def check(cls, value):
        if value is None:
            return value
        if type(value) is cls:
            return value
        try:
            return cls[cls._format_value(value)]
        except KeyError:
            return cls._missing_(value)

    def __str__(self):
        return self.value


class _Currency(_Enum):
    @property
    def value(self):
        return super(_Currency, self).value['value']

    @property
    def decimals(self):
        return super(_Currency, self).value.get('decimals', 2)


class _Market(_Enum):
    @staticmethod
    def _format_value(value):
        value = str(value).replace('-', '')
        value = f'{value[:3]}_{value[3:]}'
        return value.upper()

    @property
    def value(self):
        return super(_Market, self).value['value']

    @property
    def base(self):
        return super(_Market, self).value['base']

    @property
    def quote(self):
        return super(_Market, self).value['quote']
