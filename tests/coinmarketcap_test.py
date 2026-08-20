import unittest

from trading_api_wrappers import CoinMarketCap, InvalidResponse


class CoinMarketCapTest(unittest.TestCase):
    def setUp(self):
        self.client = CoinMarketCap()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CoinMarketCap)

    def test_ticker_list(self):
        ticker = self.client.ticker(limit=5)
        self.assertGreater(len(ticker), 1)
        self.assertIn("symbol", ticker[0].keys())

    def test_ticker_list_convert(self):
        ticker = self.client.ticker(convert="CLP", limit=5)
        self.assertGreater(len(ticker), 1)
        quotes = ticker[0]["quote"]
        if isinstance(quotes, list):
            symbols = {item["symbol"] for item in quotes}
            self.assertIn("CLP", symbols)
        else:
            self.assertIn("CLP", quotes)

    def test_ticker_currency(self):
        ticker = self.client.ticker("btc")
        self.assertEqual(ticker["symbol"], "BTC")

    def test_ticker_currency_convert(self):
        ticker = self.client.ticker("btc", "clp")
        self.assertEqual(ticker["symbol"], "BTC")
        price = self.client._quote_price(ticker, "CLP")
        self.assertIsInstance(price, float)

    def test_ticker_bad_currency(self):
        with self.assertRaises((KeyError, InvalidResponse)):
            self.client.ticker("zzznotacoinzzz")

    def test_price_currency(self):
        price = self.client.price("btc")
        self.assertIsInstance(price, float)

    def test_price_currency_convert(self):
        price = self.client.price("btc", "clp")
        self.assertIsInstance(price, float)

    def test_stats(self):
        stats = self.client.stats()
        self.assertTrue(stats)
