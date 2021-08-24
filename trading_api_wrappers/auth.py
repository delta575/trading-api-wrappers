import hmac
import json
import urllib.parse

import requests.auth
from requests import PreparedRequest as P
from requests import Response as R

from . import base


class AuthBase(requests.auth.AuthBase):
    def __call__(self, r: P):
        raise NotImplementedError("Auth hooks must be callable.")

    @staticmethod
    def check_credentials(**credentials):
        for _name, key in credentials.items():
            if not key:
                raise ValueError("{} Key and Secret are needed!")

    @staticmethod
    def url_query_split(url: str):
        _url = url.rsplit("?", 1)[0]
        query = urllib.parse.urlsplit(url).query
        return _url, query

    @staticmethod
    def parse_data(value):
        return urllib.parse.parse_qs(value)

    @staticmethod
    def load_json(value):
        return json.loads(value) if value else {}

    @staticmethod
    def encode_data(payload):
        return urllib.parse.urlencode(payload, doseq=True)

    @staticmethod
    def encode_json(payload):
        return json.dumps(payload).encode()


class ApiKeyAuth(AuthBase):
    """Attaches API KEY Authentication to the given Request object."""

    api_key_param: str = "api_key"

    def __init__(self, api_key: str, api_key_param: str = None):
        # Set credentials
        self.api_key: str = api_key
        # Override defaults
        if api_key_param is not None:
            self.api_key_param = api_key_param

    def add_api_key(self, r: P):
        # Add the API key as a query parameter
        url, query = self.url_query_split(r.url)
        params = self.parse_data(query)
        params[self.api_key_param] = self.api_key
        r.prepare_url(url, params)

    def auth_request(self, r: P):
        """Authenticate the Request"""
        self.add_api_key(r)

    def __call__(self, r: P):
        self.auth_request(r)
        return r

    def __eq__(self, other):
        return all(
            [
                self.api_key == getattr(other, "api_key", None),
            ]
        )

    def __ne__(self, other):
        return not self == other


class HMACAuth(AuthBase):
    """Attaches HMAC Authentication to the given Request object."""

    api_key_header: str = "x-auth-key"
    nonce_header: str = "x-auth-nonce"
    signature_header: str = "x-auth-signature"
    content_type_header: str = "content-type"
    signature_delimiter: str = "\n"
    algorithm = "sha256"
    timestamp: base.Timestamp = base.timestamp

    def __init__(
        self,
        api_key: str,
        secret: str,
        api_key_header: str = None,
        nonce_header: str = None,
        signature_header: str = None,
        algorithm=None,
    ):
        # Set credentials
        self.api_key: str = api_key
        self.secret: str = secret
        # Override defaults
        if api_key_header is not None:
            self.api_key_header = self.api_key_header
        if nonce_header is not None:
            self.nonce_header = self.nonce_header
        if signature_header is not None:
            self.signature_header = self.signature_header
        if algorithm is not None:
            self.algorithm = self.algorithm
        # Set counters
        self.last_nonce: int = 0
        self.num_401_calls: int = 0

    def _nonce(self):
        return self.timestamp.microseconds()

    def new_nonce(self, nonce: int = None):
        nonce = nonce or self._nonce()
        self.last_nonce = nonce
        return str(nonce)

    def add_api_key(self, r: P):
        r.headers[self.api_key_header] = self.api_key

    def add_nonce(self, r: P, nonce: str):
        r.headers[self.nonce_header] = nonce

    def add_signature(self, r: P, nonce: str):
        message = self.build_message(r, nonce)
        signature = self.sign(message)
        r.headers[self.signature_header] = signature

    def build_message(self, r: P, nonce: str):
        """Build the message to sign"""
        components = [r.method, nonce, r.path_url]
        if r.body:
            components.append(r.body)
        message = self.signature_delimiter.join(components)
        return message

    def sign(self, msg: str):
        """Sign the message"""
        encoded_msg = msg.encode() if isinstance(msg, str) else msg

        h = hmac.new(
            key=self.secret.encode(), msg=encoded_msg, digestmod=self.algorithm
        )

        signature = h.hexdigest()

        return signature

    def auth_request(self, r: P, nonce: str):
        """Authenticate the Request"""
        self.add_api_key(r)
        self.add_nonce(r, nonce)
        self.add_signature(r, nonce)

    def handle_redirect(self, r: R, **kwargs):
        """Reset num_401_calls counter on redirects."""
        if r.is_redirect:
            self.num_401_calls = 1

    def handle_401(self, r: R, **kwargs):
        """Takes the given response and re-tries auth with a new nonce."""

        if r.status_code == 401 and self.num_401_calls < 2:

            self.num_401_calls += 1

            # Renew nonce
            nonce = self.new_nonce(max(self._nonce(), self.last_nonce + 1))

            # Consume content and release the original connection
            # to allow our new request to reuse the same one.
            r.content
            r.close()
            prep = r.request.copy()
            cookies = prep._cookies
            requests.auth.extract_cookies_to_jar(cookies, r.request, r.raw)
            prep.prepare_cookies(cookies)

            self.auth_request(prep, nonce)

            _r = r.connection.send(prep, **kwargs)
            _r.history.append(r)
            _r.request = prep

            return _r

        return r

    def __call__(self, r: P):
        # Get nonce and authenticate the Request
        nonce = self.new_nonce()
        self.auth_request(r, nonce)

        # Register hooks
        r.register_hook("response", self.handle_401)
        r.register_hook("response", self.handle_redirect)

        return r

    def __eq__(self, other):
        return all(
            [
                self.api_key == getattr(other, "api_key", None),
                self.secret == getattr(other, "secret", None),
            ]
        )

    def __ne__(self, other):
        return not self == other
