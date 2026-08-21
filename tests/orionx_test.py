import unittest

from tests.helpers import env, skip_http, skip_without
from trading_api_wrappers import Orionx
from trading_api_wrappers.market import OrderBook, Quotation, Ticker


class OrionxPublicTest(unittest.TestCase):
    def setUp(self):
        self.client = Orionx.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Orionx.Public)

    @skip_http(500)
    def test_markets(self):
        markets = self.client.markets()
        self.assertGreater(len(markets), 0)

    @skip_http(500)
    def test_ticker(self):
        ticker = self.client.ticker("BTCCLP")
        self.assertIsInstance(ticker, Ticker)

    @skip_http(500)
    def test_order_book(self):
        book = self.client.order_book("BTCCLP", limit=5)
        self.assertIsInstance(book, OrderBook)
        self.assertGreater(len(book.bids) + len(book.asks), 0)

    @skip_http(500)
    def test_quotation(self):
        quoted = self.client.quotation("BTCCLP", "buy", 0.0001)
        self.assertIsInstance(quoted, Quotation)


@skip_without("ORIONX_API_KEY", "ORIONX_API_SECRET")
class OrionxAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = Orionx.Auth(env("ORIONX_API_KEY"), env("ORIONX_API_SECRET"))

    def test_ticker(self):
        ticker = self.client.ticker("BTCCLP")
        self.assertIsInstance(ticker, Ticker)
        self.assertTrue(ticker.last or ticker.bid or ticker.ask)

    def test_order_book(self):
        book = self.client.order_book("BTCCLP", limit=5)
        self.assertIsInstance(book, OrderBook)
        self.assertGreater(len(book.bids) + len(book.asks), 0)
