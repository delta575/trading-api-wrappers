import unittest

from tests.helpers import env, skip_without
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

    def test_trades(self):
        trades = self.client.trades(MARKET_ID, page_size=5)
        self.assertGreater(len(trades), 0)

    def test_quotation(self):
        quoted = self.client.quotation(MARKET_ID, "buy", 0.0001)
        self.assertGreater(quoted.base_exchanged, 0)


@skip_without("RIPIO_API_KEY", "RIPIO_API_SECRET")
class RipioAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = Ripio.Auth(env("RIPIO_API_KEY"), env("RIPIO_API_SECRET"))

    def test_balances(self):
        balances = self.client.balances()
        self.assertIsNotNone(balances)
