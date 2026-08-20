import unittest

from tests.helpers import env, skip_without
from trading_api_wrappers import NotBank
from trading_api_wrappers.market import Market, OrderBook, Ticker, Trade


class NotBankPublicTest(unittest.TestCase):
    def setUp(self):
        self.client = NotBank.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, NotBank.Public)

    def test_markets(self):
        markets = self.client.markets()
        self.assertGreater(len(markets), 0)
        self.assertIsInstance(markets[0], Market)
        symbols = {market.id for market in markets}
        self.assertIn("BTCCLP", symbols)

    def test_ticker(self):
        ticker = self.client.ticker("BTCCLP")
        self.assertIsInstance(ticker, Ticker)
        self.assertTrue(ticker.last or ticker.bid or ticker.ask)

    def test_order_book(self):
        book = self.client.order_book("BTCCLP", depth=5)
        self.assertIsInstance(book, OrderBook)
        self.assertGreater(len(book.bids) + len(book.asks), 0)

    def test_trades(self):
        trades = self.client.trades("BTCCLP", limit=5)
        self.assertIsInstance(trades, list)
        if trades:
            self.assertIsInstance(trades[0], Trade)


@skip_without("NOTBANK_API_KEY", "NOTBANK_API_SECRET", "NOTBANK_USER_ID")
class NotBankAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = NotBank.Auth(
            env("NOTBANK_API_KEY"),
            env("NOTBANK_API_SECRET"),
            env("NOTBANK_USER_ID"),
        )

    def test_balances(self):
        balances = self.client.balances()
        self.assertIsNotNone(balances)
