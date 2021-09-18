import asyncio
import json as j
import time
from enum import Enum
from json.decoder import JSONDecodeError
from typing import Iterable
from urllib.parse import urljoin

import backoff
import requests
from requests import Response, Session
from requests.auth import AuthBase
from requests_toolbelt import user_agent as ua

from ._version import __version__
from .common import clean_empty
from .errors import DecodeError, InvalidResponse, RequestException

TIMEOUT = 30
RETRY_CODES = [
    400,
    401,
    403,
    404,
    408,
    429,
    500,
    502,
    503,
    504,
]


class Timestamp:
    @staticmethod
    def seconds():
        return int(time.time())

    @staticmethod
    def milliseconds():
        return int(time.time() * 1e3)

    @staticmethod
    def microseconds():
        return int(time.time() * 1e6)


timestamp = Timestamp()


class ClientSession(Session):
    user_agent = ua("trading-api-wrappers", __version__)

    def __init__(self, base_url: str, timeout: int = TIMEOUT, user_agent: str = None):
        # Init session
        super().__init__()
        # Instance attributes
        self.auth: AuthBase = None
        self.base_url: str = base_url
        self.timeout: int = timeout
        self.last_nonce: int = 0
        self.last_request_timestamp: int = 0
        if user_agent is not None:
            self.user_agent = user_agent

    def request(self, method, endpoint, *args, **kwargs):
        """Send the request after generating the complete URL."""
        kwargs.setdefault("allow_redirects", True)
        url = self.url_for(endpoint)
        # Clean empty values
        for key in ["data", "json", "params"]:
            value = kwargs.get(key)
            if value:
                cleaned = clean_empty(value)
                kwargs[key] = cleaned
        # Set default user-agent
        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = self.user_agent
        # Send the request
        return super().request(
            method,
            url,
            headers=headers,
            auth=self.auth,
            timeout=self.timeout,
            *args,
            **kwargs,
        )

    def url_for(self, endpoint: str):
        """Create the URL based off this partial endpoint."""
        return urljoin(self.base_url, endpoint)


class Client:
    base_url: str = ""
    error_keys: Iterable[str] = []
    rate_limit: int = 0  # in milliseconds
    session_cls = ClientSession
    timestamp: Timestamp = timestamp
    retry_codes: Iterable[int] = RETRY_CODES
    # Client defaults
    enable_rate_limit: bool = True
    backoff_factor: float = 1.5  # in seconds
    max_retries: int = 3
    timeout: int = TIMEOUT

    def __init__(
        self,
        timeout: int = None,
        max_retries: int = None,
        backoff_factor: float = None,
        rate_limit: int = None,
        user_agent: str = None,
        base_url: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        # Override defaults
        if timeout is not None:
            self.timeout = timeout
        if max_retries is not None:
            self.max_retries = max_retries
        if rate_limit is not None:
            self.rate_limit = rate_limit
        if backoff_factor is not None:
            self.backoff_factor = backoff_factor
        if base_url is not None:
            self.base_url = base_url
        # Create session
        self.session: ClientSession = self.session_cls(
            self.base_url, self.timeout, user_agent
        )
        # Attributes
        self.last_request_timestamp: int = 0

    def get(self, endpoint, **kwargs):
        return self._fetch("GET", endpoint, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        return self._fetch("POST", endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint, data=None, **kwargs):
        return self._fetch("PUT", endpoint, data=data, **kwargs)

    def patch(self, endpoint, data=None, **kwargs):
        return self._fetch("PATCH", endpoint, data=data, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._fetch("DELETE", endpoint, **kwargs)

    def _retry(self, target):
        # Verify that sync version is not being run from coroutine
        # Backoff can't run inside a coroutine.
        try:
            asyncio.get_event_loop()
        except RuntimeError:
            # Event loop not set for this thread.
            return target

        def give_up_retry(e: RequestException):
            give_up = False
            if e.response:
                code = e.response.status_code
                give_up = code not in self.retry_codes
            return give_up

        return backoff.on_exception(
            backoff.expo,
            RequestException,
            factor=self.backoff_factor,
            max_time=self.timeout,
            max_tries=self.max_retries,
            giveup=give_up_retry,
        )(target)

    def _fetch(self, method, endpoint, *args, **kwargs):
        @self._retry
        def fetch():
            return self._fetch_base(method, endpoint, *args, **kwargs)

        return fetch()

    def _fetch_base(self, method, endpoint, *args, **kwargs):
        # Rate limit requests
        if self.rate_limit:
            self.throttle()
        self.last_request_timestamp = self.timestamp.milliseconds()
        # Send the request
        response = self.session.request(method, endpoint, *args, **kwargs)
        # Check response for errors
        try:
            response.raise_for_status()
        except requests.HTTPError:
            error_msg = self._get_error_message(response)
            raise InvalidResponse(error_msg, response)
        # Decode the response
        json = self._decode_response(response)
        return json

    def _get_error_message(self, data):
        for error_key in self.error_keys:
            try:
                json = data.json() if isinstance(data, Response) else data
                message = json[error_key]
                if message:
                    msg = j.dumps(message).replace('"', "").rstrip(".")
                    msg = f"{error_key}: {msg}"
                    return msg
            except (JSONDecodeError, KeyError, TypeError):
                continue

    def _decode_response(self, response):
        try:
            json = response.json()
        except JSONDecodeError as e:
            error_msg = "Unable to decode JSON from response (no content)"
            raise DecodeError(error_msg, response) from e
        error_msg = self._get_error_message(json)
        if error_msg:
            raise InvalidResponse(error_msg, response)
        return json

    def throttle(self):
        now = float(self.timestamp.milliseconds())
        elapsed = now - self.last_request_timestamp
        if elapsed < self.rate_limit:
            delay = self.rate_limit - elapsed
            time.sleep(delay / 1e3)

    def __del__(self):
        if self.session:
            self.session.close()


class AuthMixin:
    auth_cls = None

    @property
    def auth(self):
        return self.session.auth

    @auth.setter
    def auth(self, auth: AuthBase):
        self.session.auth = auth

    def add_auth(self, *credentials):
        self.auth = self.auth_cls(*credentials)


class ModelMixin:
    return_json: bool = False

    def __init__(self, return_json: bool = None):
        super().__init__()
        if return_json is not None:
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
        return super().value["value"]

    @property
    def decimals(self):
        return super().value.get("decimals", 2)


class Market(_Enum):
    @staticmethod
    def _format_value(value):
        value = str(value).replace("-", "")
        value = f"{value[:3]}_{value[3:]}"
        return value.upper()

    @property
    def value(self):
        return super().value["value"]

    @property
    def base(self):
        return super().value["base"]

    @property
    def quote(self):
        return super().value["quote"]
