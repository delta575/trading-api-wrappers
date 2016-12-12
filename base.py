from urllib.parse import urlparse
import json
# pip
import requests
# local
from common import check_response


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
        response = requests.get(url, headers=headers, params=params, verify=True, timeout=self.TIMEOUT)
        json_resp = response.json()
        check_response(json_resp)
        return json_resp

    def put(self, url, headers, data):
        response = requests.put(url, headers=headers, data=json.dumps(data), verify=True, timeout=self.TIMEOUT)
        json_resp = response.json()
        check_response(json_resp)
        return json_resp

    def post(self, url, headers, data):
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=True, timeout=self.TIMEOUT)
        json_resp = response.json()
        check_response(json_resp)
        return json_resp

    def url_for(self, path, path_arg=None):
        url = '{0:s}/{1:s}'.format(self.SERVER.URL, path)
        if path_arg:
            url = url % path_arg
        return url

    def url_path_for(self, path, path_arg=None):
        url = self.url_for(path, path_arg)
        path = urlparse(url).path
        return url, path
