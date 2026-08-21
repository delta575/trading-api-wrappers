import unittest

from tests.helpers import env, skip_http, skip_without
from trading_api_wrappers import Bybit
from trading_api_wrappers.market import (
    Candlestick,
    Market,
    OrderBook,
    Quotation,
    Ticker,
    Trade,
)

SYMBOL = "BTCUSDT"


class BybitPublicTest(unittest.TestCase):
    def setUp(self):
        self.client = Bybit.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bybit.Public)

    @skip_http(403, 451)
    def test_markets(self):
        markets = self.client.markets()
        self.assertGreater(len(markets), 0)
        self.assertIsInstance(markets[0], Market)

    @skip_http(403, 451)
    def test_ticker(self):
        ticker = self.client.ticker(SYMBOL)
        self.assertIsInstance(ticker, Ticker)
        self.assertTrue(ticker.last or ticker.bid or ticker.ask)

    @skip_http(403, 451)
    def test_order_book(self):
        book = self.client.order_book(SYMBOL, limit=5)
        self.assertIsInstance(book, OrderBook)
        self.assertGreater(len(book.bids) + len(book.asks), 0)

    @skip_http(403, 451)
    def test_trades(self):
        trades = self.client.trades(SYMBOL, limit=5)
        self.assertIsInstance(trades, list)
        if trades:
            self.assertIsInstance(trades[0], Trade)

    @skip_http(403, 451)
    def test_candles(self):
        candles = self.client.candles(SYMBOL, interval="60", limit=3)
        self.assertGreater(len(candles), 0)
        self.assertIsInstance(candles[0], Candlestick)

    @skip_http(403, 451)
    def test_quotation(self):
        quoted = self.client.quotation(SYMBOL, "buy", 0.001)
        self.assertIsInstance(quoted, Quotation)
        self.assertGreater(quoted.base_exchanged, 0)


@skip_without("BYBIT_API_KEY", "BYBIT_API_SECRET")
class BybitAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = Bybit.Auth(env("BYBIT_API_KEY"), env("BYBIT_API_SECRET"))

    @skip_http(403, 451)
    def test_balances(self):
        balances = self.client.balances()
        self.assertIsNotNone(balances)
