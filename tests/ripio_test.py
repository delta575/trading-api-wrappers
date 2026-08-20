import unittest

from trading_api_wrappers import Ripio
from trading_api_wrappers.ripio import models
from trading_api_wrappers.ripio.clients import RipioExchangePublic

MARKET_ID = "BTC_BRL"


class RipioPublicTest(unittest.TestCase):
    def setUp(self):
        self.client = Ripio.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Ripio.Public)

    def test_rates_raw(self):
        rates = self.client.rates_raw()
        self.assertEqual(
            sorted(["base", "rates", "names", "variation"]), sorted(list(rates.keys()))
        )

    def test_rates(self):
        rates = self.client.rates()
        self.assertIsInstance(rates, models.Rates)


class RipioExchangePublicTest(unittest.TestCase):
    def setUp(self):
        self.client = Ripio.Public().exchange

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, RipioExchangePublic)

    def test_tickers(self):
        tickers = self.client.tickers()
        self.assertGreater(len(tickers), 0)
        self.assertIn("pair", tickers[0])

    def test_order_book(self):
        order_book = self.client.order_book(MARKET_ID, limit=5)
        self.assertIsInstance(order_book, models.OrderBook)
        self.assertGreater(len(order_book.bids) + len(order_book.asks), 0)
