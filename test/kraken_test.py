import unittest

# pip
from decouple import config

# local
from trading_api_wrappers import errors, Kraken

API_KEY = config('KRAKEN_API_KEY')
API_SECRET = config('KRAKEN_API_SECRET')


class KrakenPublicTest(unittest.TestCase):

    def setUp(self):
        self.client = Kraken.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Kraken.Public)

    def test_server_time(self):
        response = self.client.server_time()
        self.assertIn('result', response.keys())


class KrakenAuthTest(unittest.TestCase):

    def setUp(self):
        self.client = Kraken.Auth(API_KEY, API_SECRET)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Kraken.Auth)

    def test_balance(self):
        response = self.client.balance()
        self.assertIn('result', response.keys())

    def test_trade_balance(self):
        response = self.client.trade_balance()
        self.assertIn('result', response.keys())

    def test_error(self):
        self.assertRaises(errors.InvalidResponse,
                          lambda: self.client.trades('ERROR'))
