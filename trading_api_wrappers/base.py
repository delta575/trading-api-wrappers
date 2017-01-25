import json
from urllib.parse import urlparse

# pip
import requests
# local
from trading_api_wrappers.common import (check_response, log_json_decode,
                                         log_request_exception)


class Server(object):

    def __init__(self, protocol, host, version=None):
        url = '{0:s}://{1:s}'.format(protocol, host)
        if version:
            url = '{0:s}/{1:s}'.format(url, version)

        self.PROTOCOL = protocol
        self.HOST = host
        self.VERSION = version
        self.URL = url


class Client(object):

    def __init__(self, server: Server, timeout=30):
        self.SERVER = server
        self.TIMEOUT = timeout

    def get(self, url, headers=None, params=None):
        response = self._request('get', url, headers=headers, params=params)
        json_resp = self._resp_to_json(response)
        return json_resp

    def put(self, url, headers, data):
        response = self._request('put', url, headers=headers, data=data)
        json_resp = self._resp_to_json(response)
        return json_resp

    def post(self, url, headers, data):
        response = self._request('post', url, headers=headers, data=data)
        json_resp = self._resp_to_json(response)
        return json_resp

    def _request(self, method, url, headers, params=None, data=None):
        try:
            data = json.dumps(data) if data else data
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                data=data,
                verify=True,
                timeout=self.TIMEOUT)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as err:
            log_request_exception(err)
            raise

    def _resp_to_json(self, response):
        try:
            json_resp = response.json()
            check_response(json_resp)
            return json_resp
        except json.decoder.JSONDecodeError:
            log_json_decode()
            raise

    def url_for(self, path, path_arg=None):
        url = '{0:s}/{1:s}'.format(self.SERVER.URL, path)
        if path_arg:
            url = url % path_arg
        return url

    def url_path_for(self, path, path_arg=None):
        url = self.url_for(path, path_arg)
        path = urlparse(url).path
        return url, path
