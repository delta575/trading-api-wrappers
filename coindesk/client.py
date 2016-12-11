from common import Client

# API Server
PROTOCOL = 'https'
HOST = 'api.coindesk.com'
VERSION = 'v1'

# API Paths
PATH_BPI = 'bpi/currentprice/%s.json'
PATH_HISTORICAL = 'bpi/historical/close.json'


class CoinDesk(object):
    
    def __init__(self, timeout=15):
        self.client = Client(PROTOCOL, HOST, VERSION, timeout)    

    def current_bpi(self, currency):
        """Gets the Bitcoin Price Index (BPI) in real-time for the specified currency.

        GET http(s)://api.coindesk.com/v1/bpi/currentprice/[currency].json

        Args:
            currency (str): One of the supported currency codes.
                http://api.coindesk.com/v1/bpi/supported-currencies.json

        Returns:
            dict: A dictionary with the following (example):

            {
                'time': {
                    'updatedISO': '2016-12-11T17:39:00+00:00',
                    'updated': 'Dec 11, 2016 17:39:00 UTC',
                    'updateduk': 'Dec 11, 2016 at 17:39 GMT'
                    },
                'bpi': {
                    'BTC': {
                        'rate': '1.0000',
                        'rate_float': 1,
                        'code': 'BTC',
                        'description': 'Bitcoin'
                    },
                    'USD': {
                        'rate': '768.4125',
                        'rate_float': 768.4125,
                        'code': 'USD',
                        'description': 'United States Dollar'
                    }
                },
                'disclaimer': 'Disclaimer text.'
            }

        """
        url = self.client.url_for(PATH_BPI, path_arg=currency)
        return self.client.get(url)

    def historical_bpi(self, index=None, currency=None, start=None, end=None, yesterday=None):
        """Gets the hstorical Bitcoin Price Index (BPI) for the specified currency.

        GET http(s)://api.coindesk.com/v1/bpi/historical/close.json

        Args:
            index (str):
                [USD/CNY] The index to return data for. Defaults to USD.

            currency (str):
                The currency to return the data in, specified in ISO 4217 format. Defaults to USD.

            start (datetime):
                Allows data to be returned for a specific date range.
                Must be listed as a pair of start and end parameters, with dates supplied in the YYYY-MM-DD format,
                e.g. 2013-09-01 for September 1st, 2013.

            end (datetime):
                Allows data to be returned for a specific date range.
                Must be listed as a pair of start and end parameters, with dates supplied in the YYYY-MM-DD format,
                e.g. 2013-09-01 for September 1st, 2013.

            yesterday (bool):
                Specifying this will return a single value for the previous day. Overrides the start/end parameter.

        Returns:
            dict: A dictionary with the following (example):

            {
                'time': {
                    'updatedISO': '2016-12-11T00:03:00+00:00',
                    'updated': 'Dec 11, 2016 00:03:00 UTC'
                },
                'bpi': {
                    '2016-11-20': 728.6075,
                    '2016-11-21': 736.7163,
                    '2016-11-15': 711.9563,
                    ...
                },
                'disclaimer': 'Disclaimer text.'
            }

        """
        parameters = {
            'index': index,
            'currency': currency,
            'start': start,
            'end': end,
            'for': 'yesterday' if yesterday else None,
        }
        url = self.client.url_for(PATH_HISTORICAL)
        return self.client.get(url, params=parameters)
