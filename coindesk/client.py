import requests
import json

PROTOCOL = "https"
HOST = "api.coindesk.com"
VERSION = "v1"

PATH_BPI = "bpi/currentprice/"
PATH_HISTORICAL = 'bpi/historical/close.json?currency='

# HTTP request timeout in seconds
TIMEOUT = 15.0


class CDClient(object):
    def server(self):
        return "%s://%s/%s" % (PROTOCOL, HOST, VERSION)

    def url_for(self, path, path_arg=None, parameters=None):
        url = "%s/%s" % (self.server(), path)

        if path_arg:
            url = url % (path_arg)

        if parameters:
            url = "%s?%s" % (url, self._build_parameters(parameters))

        return url

    def getBPI(self, currency):
        try:
            data = self._get(self.url_for(PATH_BPI + currency))
            return data
        except:
            return 'error'

    def volex(self):
        data = requests.get('https://btcvol.info/latest', timeout=TIMEOUT).json()
        return data

    def histData(self, currency):
        data = self._get(self.url_for(PATH_HISTORICAL + currency))
        return data

    def _get(self, url):
        return requests.get(url, timeout=TIMEOUT).json()

    def _build_parameters(self, parameters):
        # sort the keys so we can test easily in Python 3.3 (dicts are not ordered)
        keys = list(parameters.keys())
        keys.sort()
        return '&'.join(["%s=%s" % (k, parameters[k]) for k in keys])