import unittest

from tests.helpers import env, skip_without
from trading_api_wrappers import Bitso
from trading_api_wrappers.market import (
    Candlestick,
    Market,
    OrderBook,
    Quotation,
    Ticker,
    Trade,
)

BOOK = "btc_mxn"


class BitsoPublicTest(unittest.TestCase):
    def setUp(self):
        self.client = Bitso.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitso.Public)

    def test_markets(self):
        markets = self.client.markets()
        self.assertGreater(len(markets), 0)
        self.assertIsInstance(markets[0], Market)
        self.assertIn(BOOK, {market.id for market in markets})

    def test_ticker(self):
        ticker = self.client.ticker(BOOK)
        self.assertIsInstance(ticker, Ticker)
        self.assertTrue(ticker.last)

    def test_order_book(self):
        book = self.client.order_book(BOOK)
        self.assertIsInstance(book, OrderBook)
        self.assertGreater(len(book.bids) + len(book.asks), 0)

    def test_trades(self):
        trades = self.client.trades(BOOK, limit=5)
        self.assertIsInstance(trades, list)
        if trades:
            self.assertIsInstance(trades[0], Trade)

    def test_candles(self):
        candles = self.client.candles(BOOK, time_bucket=3600)
        self.assertGreater(len(candles), 0)
        self.assertIsInstance(candles[0], Candlestick)

    def test_quotation(self):
        quoted = self.client.quotation(BOOK, "bid_given_size", 0.0001)
        self.assertIsInstance(quoted, Quotation)
        self.assertEqual(quoted.side, "buy")
        self.assertGreater(quoted.base_exchanged, 0)


@skip_without("BITSO_API_KEY", "BITSO_API_SECRET")
class BitsoAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = Bitso.Auth(env("BITSO_API_KEY"), env("BITSO_API_SECRET"))

    def test_balances(self):
        balances = self.client.balances()
        self.assertIsNotNone(balances)
