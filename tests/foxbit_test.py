import unittest

from tests.helpers import env, skip_without
from trading_api_wrappers import Foxbit
from trading_api_wrappers.market import (
    Candlestick,
    Market,
    OrderBook,
    Quotation,
    Ticker,
    Trade,
)

SYMBOL = "btcbrl"


class FoxbitPublicTest(unittest.TestCase):
    def setUp(self):
        self.client = Foxbit.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Foxbit.Public)

    def test_markets(self):
        markets = self.client.markets()
        self.assertGreater(len(markets), 0)
        self.assertIsInstance(markets[0], Market)
        self.assertIn(SYMBOL, {market.id for market in markets})

    def test_ticker(self):
        ticker = self.client.ticker(SYMBOL)
        self.assertIsInstance(ticker, Ticker)
        self.assertTrue(ticker.last or ticker.bid or ticker.ask)

    def test_order_book(self):
        book = self.client.order_book(SYMBOL, depth=5)
        self.assertIsInstance(book, OrderBook)
        self.assertGreater(len(book.bids) + len(book.asks), 0)

    def test_trades(self):
        trades = self.client.trades(SYMBOL, page_size=5)
        self.assertIsInstance(trades, list)
        if trades:
            self.assertIsInstance(trades[0], Trade)

    def test_candles(self):
        candles = self.client.candles(SYMBOL, interval="1h", limit=3)
        self.assertGreater(len(candles), 0)
        self.assertIsInstance(candles[0], Candlestick)

    def test_quotation(self):
        quoted = self.client.quotation(SYMBOL, "buy", 0.0001)
        self.assertIsInstance(quoted, Quotation)
        self.assertGreater(quoted.base_exchanged, 0)


@skip_without("FOXBIT_API_KEY", "FOXBIT_API_SECRET")
class FoxbitAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = Foxbit.Auth(env("FOXBIT_API_KEY"), env("FOXBIT_API_SECRET"))

    def test_balances(self):
        balances = self.client.balances()
        self.assertIsNotNone(balances)
