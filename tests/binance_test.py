import unittest

from tests.helpers import env, skip_http, skip_without
from trading_api_wrappers import Binance
from trading_api_wrappers.market import Market, OrderBook, Ticker, Trade

SYMBOL = "BTCUSDT"


class BinancePublicTest(unittest.TestCase):
    def setUp(self):
        self.client = Binance.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Binance.Public)

    @skip_http(403, 451)
    def test_markets(self):
        markets = self.client.markets()
        self.assertGreater(len(markets), 0)
        self.assertIsInstance(markets[0], Market)

    @skip_http(403, 451)
    def test_ticker(self):
        ticker = self.client.ticker(SYMBOL)
        self.assertIsInstance(ticker, Ticker)
        self.assertTrue(ticker.last)

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


@skip_without("BINANCE_API_KEY", "BINANCE_API_SECRET")
class BinanceAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = Binance.Auth(env("BINANCE_API_KEY"), env("BINANCE_API_SECRET"))

    @skip_http(403, 451)
    def test_account(self):
        account = self.client.account()
        self.assertIn("balances", account)
