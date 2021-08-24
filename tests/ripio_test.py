import unittest

from trading_api_wrappers import Ripio
from trading_api_wrappers.ripio import models
from trading_api_wrappers.ripio.clients import RipioExchangePublic

MARKET_ID = "ARS/BTC"


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

    def test_order_books(self):
        order_books = self.client.order_books()
        for order_book in order_books.values():
            self.assertIsInstance(order_book, models.OrderBook)

    def test_order_book(self):
        order_book = self.client.order_book(MARKET_ID)
        self.assertIsInstance(order_book, models.OrderBook)
