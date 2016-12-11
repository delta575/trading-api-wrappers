from urllib.parse import urlparse, urlencode
import json
import time
# pip
import requests


class Client(object):

    def __init__(self, protocol, host, version, timeout=30):
        self.URL = '{0:s}://{1:s}/{2:s}'.format(protocol, host, version)
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
        url = '{0:s}/{1:s}'.format(self.URL, path)
        if path_arg:
            url = url % path_arg
        return url

    def url_path_for(self, path, path_arg=None):
        url = self.url_for(path, path_arg)
        path = urlparse(url).path
        return url, path


def gen_nonce():
    # Sleeps 200ms to avoid flooding the server with requests.
    time.sleep(0.2)
    # Get a str from the current time in microseconds.
    return str(int(time.time() * 1E6))


def check_keys(key, secret):
    if not key or not secret:
        raise ValueError('API Key and Secret are needed!')


def check_response(response):
    if 'message' in response:
        raise Exception(response['message'])


def build_parameters(parameters):
    if parameters:
        p = {k: v for k, v in parameters.items() if v is not None}
        return urlencode(p, True)
    else:
        return None


def build_route(path, params=None):
    built_params = build_parameters(params)
    if built_params:
        return '{0:s}?{1:s}'.format(path, built_params)
    else:
        return path


def update_dictionary(old_dict: dict, new_dict: dict):
    if new_dict:
        keys = list(new_dict.keys())
        for k in keys:
            old_dict[k] = new_dict[k]
