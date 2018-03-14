import json
import requests
from datetime import datetime
from ..base import Client, Server
from ..common import check_keys
from base64 import standard_b64encode


# API Server
PROTOCOL = 'https'
HOST = 'v2.api.xapo.com'

# PROTOCOL = 'http'
# HOST = 'localhost:8080'

class XapoStandard(Client):
    def _get(self, url):
            headers = {'Authorization': '%s %s' % (self.token_type, self.token)}
            return self.get(url, headers=headers)

    def get_token(self, key, secret):
        url, path = self.url_path_for('oauth2/token')
        authorization = 'Basic %s' % standard_b64encode(bytes(self.KEY + ":" + self.SECRET, "utf-8")).decode()
        headers = {'Authorization': authorization, 'Content-Type': 'application/x-www-form-urlencoded'}
        body = {'grant_type': 'client_credentials', 'redirect_uri': 'http://test.antarcticx.com'}
        response_json = requests.post(
            url, headers=headers,
            data=body
        ).json()
        return response_json['token_type'], response_json['access_token']


    def __init__(self, key=False, secret=False, timeout=30):
        server = Server(PROTOCOL, HOST)
        Client.__init__(self, server, timeout)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)
        self.token_type, self.token = self.get_token(self.KEY, self.SECRET)


    def _get_accounts(self):
        url, path = self.url_path_for('accounts')
        response = self._get(url)
        print("hola")

