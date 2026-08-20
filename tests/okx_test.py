import unittest

from tests.helpers import env, skip_without
from trading_api_wrappers import OKX
from trading_api_wrappers.market import Market, OrderBook, Ticker, Trade

SYMBOL = "BTC-USDT"


class OKXPublicTest(unittest.TestCase):
    def setUp(self):
        self.client = OKX.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, OKX.Public)

    def test_markets(self):
        markets = self.client.markets()
        self.assertGreater(len(markets), 0)
        self.assertIsInstance(markets[0], Market)

    def test_ticker(self):
        ticker = self.client.ticker(SYMBOL)
        self.assertIsInstance(ticker, Ticker)
        self.assertTrue(ticker.last)

    def test_order_book(self):
        book = self.client.order_book(SYMBOL, sz=5)
        self.assertIsInstance(book, OrderBook)
        self.assertGreater(len(book.bids) + len(book.asks), 0)

    def test_trades(self):
        trades = self.client.trades(SYMBOL, limit=5)
        self.assertIsInstance(trades, list)
        if trades:
            self.assertIsInstance(trades[0], Trade)


@skip_without("OKX_API_KEY", "OKX_API_SECRET", "OKX_PASSPHRASE")
class OKXAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = OKX.Auth(
            env("OKX_API_KEY"), env("OKX_API_SECRET"), env("OKX_PASSPHRASE")
        )

    def test_balances(self):
        balances = self.client.balances()
        self.assertIsNotNone(balances)
