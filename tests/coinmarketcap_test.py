import unittest

from trading_api_wrappers import CoinMarketCap


class CoinMarketCapTest(unittest.TestCase):
    def setUp(self):
        self.client = CoinMarketCap()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CoinMarketCap)

    # Test Ticker -------------------------------------------------------------
    def test_ticker_list(self):
        ticker = self.client.ticker()
        self.assertGreater(len(ticker), 1)
        self.assertIn("symbol", ticker[0].keys())

    def test_ticker_list_convert(self):
        ticker = self.client.ticker(convert="clp")
        self.assertGreater(len(ticker), 1)
        self.assertIn("price_clp", ticker[0].keys())

    def test_ticker_currency(self):
        ticker = self.client.ticker("btc")
        self.assertIn("symbol", ticker.keys())

    def test_ticker_currency_convert(self):
        ticker = self.client.ticker("btc", "clp")
        self.assertIn("price_clp", ticker.keys())

    def test_ticker_bad_currency(self):
        self.assertRaises(KeyError, lambda: self.client.ticker("clp"))

    # Test Ticker -------------------------------------------------------------
    def test_price_currency(self):
        price = self.client.price("btc")
        self.assertIsInstance(price, float)

    def test_price_currency_convert(self):
        price = self.client.price("btc", "clp")
        self.assertIsInstance(price, float)

    def test_price_bad_currency(self):
        self.assertRaises(KeyError, lambda: self.client.price("clp"))
