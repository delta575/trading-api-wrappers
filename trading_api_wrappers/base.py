import json as j
import time
from enum import Enum
from json.decoder import JSONDecodeError
from urllib.parse import urljoin

import requests
from requests import Response
from requests import Session
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase
from urllib3.util.retry import Retry

from . import errors
from .common import clean_empty

TIMEOUT = 30
RETRY = Retry(
    total=3,
    backoff_factor=2,
    status_forcelist=[
        400, 401, 403, 404, 408, 429,
        500, 502, 503, 504,
    ],
)

RetryTypes = (bool, int, Retry)


class Timestamp(object):

    @staticmethod
    def seconds():
        return int(time.time())

    @staticmethod
    def milliseconds():
        return int(time.time() * 1E3)

    @staticmethod
    def microseconds():
        return int(time.time() * 1E6)


timestamp = Timestamp()


class ClientSession(Session):

    def __init__(self,
                 base_url: str,
                 timeout: int=TIMEOUT,
                 retry: RetryTypes=RETRY):
        # Init session
        super().__init__()
        # Instance attributes
        self.auth: AuthBase = None
        self.base_url: str = base_url
        self.timeout: int = timeout
        self.last_nonce: int = 0
        self.last_request_timestamp: int = 0
        # Set retry configuration
        if retry is True:
            retry = RETRY
        adapter = HTTPAdapter(max_retries=retry)
        self.mount('http://', adapter)
        self.mount('https://', adapter)

    def request(self, method, endpoint, *args, **kwargs):
        """Send the request after generating the complete URL."""
        kwargs.setdefault('allow_redirects', True)
        url = self.url_for(endpoint)
        return super().request(
            method, url,
            auth=self.auth,
            timeout=self.timeout,
            *args, **kwargs,
        )

    def url_for(self, endpoint: str):
        """Create the URL based off this partial endpoint."""
        return urljoin(self.base_url, endpoint)


class Client(object):
    base_url: str = ''
    error_key: str = ''
    rate_limit: int = 1000  # in milliseconds
    session_cls = ClientSession
    timestamp: Timestamp = timestamp
    # Client defaults
    timeout: int = TIMEOUT
    retry: RetryTypes = False  # RETRY
    enable_rate_limit: bool = True

    def __init__(self,
                 timeout: int=None,
                 retry: RetryTypes=None,
                 enable_rate_limit: bool=True,
                 **kwargs):
        super().__init__(**kwargs)
        # Override defaults
        if timeout is not None:
            self.timeout = timeout
        if retry is not None:
            self.retry = retry
        if enable_rate_limit is not None:
            self.enable_rate_limit = enable_rate_limit
        # Create session
        self.session: ClientSession = self.session_cls(
            self.base_url, self.timeout, self.retry)
        # Attributes
        self.last_request_timestamp: int = 0

    def get(self, endpoint, **kwargs):
        return self._fetch('GET', endpoint, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        return self._fetch('POST', endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint, data=None, **kwargs):
        return self._fetch('PUT', endpoint, data=data, **kwargs)

    def patch(self, endpoint, data=None, **kwargs):
        return self._fetch('PATCH', endpoint, data=data, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._fetch('DELETE', endpoint, **kwargs)

    def _fetch(self, method, endpoint, *args, **kwargs):
        # Clean empty values
        for key in ['data', 'json', 'params']:
            value = kwargs.get(key)
            if value:
                cleaned = clean_empty(value)
                kwargs[key] = cleaned
        # Rate limit requests
        if self.enable_rate_limit:
            self.throttle()
        self.last_request_timestamp = self.timestamp.milliseconds()
        # Send the request
        response = self.session.request(method, endpoint, *args, **kwargs)
        # Check response for errors
        try:
            response.raise_for_status()
        except requests.HTTPError:
            error_msg = self._get_error_message(response)
            raise errors.InvalidResponse(self.error_key, error_msg, response)
        # Decode the response
        json = self._decode_response(response)
        return json

    def _get_error_message(self, data):
        if not self.error_key:
            return
        try:
            json = data.json() if isinstance(data, Response) else data
            message = json[self.error_key]
            if message:
                return j.dumps(message).replace('"', '').rstrip('.')
        except (JSONDecodeError, KeyError, TypeError):
            return

    def _decode_response(self, response):
        try:
            json = response.json()
        except JSONDecodeError as e:
            error_msg = 'Unable to decode JSON from response (no content)'
            raise errors.DecodeError(error_msg, response) from e
        error_msg = self._get_error_message(json)
        if error_msg:
            raise errors.InvalidResponse(self.error_key, error_msg, response)
        return json

    def throttle(self):
        now = float(self.timestamp.milliseconds())
        elapsed = now - self.last_request_timestamp
        if elapsed < self.rate_limit:
            delay = self.rate_limit - elapsed
            time.sleep(delay / 1E3)

    def __del__(self):
        if self.session:
            self.session.close()


class AuthMixin(object):
    auth_cls = None

    @property
    def auth(self):
        return self.session.auth

    @auth.setter
    def auth(self, auth: AuthBase):
        self.session.auth = auth

    def add_auth(self, *credentials):
        self.auth = self.auth_cls(*credentials)


class ModelMixin(object):
    return_json: bool = False

    def __init__(self, return_json: bool=None):
        super().__init__()
        if return_json:
            self.return_json = return_json


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


class Currency(_Enum):
    @property
    def value(self):
        return super().value['value']

    @property
    def decimals(self):
        return super().value.get('decimals', 2)


class Market(_Enum):
    @staticmethod
    def _format_value(value):
        value = str(value).replace('-', '')
        value = f'{value[:3]}_{value[3:]}'
        return value.upper()

    @property
    def value(self):
        return super().value['value']

    @property
    def base(self):
        return super().value['base']

    @property
    def quote(self):
        return super().value['quote']
