import unittest

from trading_api_wrappers import Bitcoinity

CURRENCY = "USD"
EXCHANGE = "bitfinex"


class BitcoinityTest(unittest.TestCase):
    def setUp(self):
        self.client = Bitcoinity()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitcoinity)

    def test_ticker_returns_data(self):
        ticker = self.client.ticker(currency=CURRENCY, exchange=EXCHANGE, span="1d")
        self.assertIn("ticker_life", ticker.keys())
