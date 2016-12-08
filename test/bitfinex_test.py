import unittest
from decouple import config

from bitfinex import Bitfinex

TEST = config('TEST', cast=bool, default=False)
API_KEY = config('BFX_API_KEY')
API_SECRET = config('BFX_API_SECRET')
SYMBOL = 'btcusd'


class BitfinexTest(unittest.TestCase):

    def setUp(self):
        self.client = Bitfinex(API_KEY, API_SECRET)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitfinex)

    def test_ticker_returns_data(self):
        markets = self.client.ticker()
        self.assertIn('last_price', markets.keys())


class BitfinexTestBadApi(unittest.TestCase):

    def setUp(self):
        self.client = Bitfinex('BAD_KEY', 'BAD_SECRET')

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitfinex)
