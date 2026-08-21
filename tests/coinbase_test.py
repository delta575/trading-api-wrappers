import unittest

from tests.helpers import env, skip_without
from trading_api_wrappers import Coinbase
from trading_api_wrappers.market import (
    Candlestick,
    Market,
    OrderBook,
    Quotation,
    Ticker,
    Trade,
)

SYMBOL = "BTC-USD"


class CoinbasePublicTest(unittest.TestCase):
    def setUp(self):
        self.client = Coinbase.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Coinbase.Public)

    def test_markets(self):
        markets = self.client.markets()
        self.assertGreater(len(markets), 0)
        self.assertIsInstance(markets[0], Market)

    def test_ticker(self):
        ticker = self.client.ticker(SYMBOL)
        self.assertIsInstance(ticker, Ticker)
        self.assertTrue(ticker.last or ticker.bid or ticker.ask)

    def test_order_book(self):
        book = self.client.order_book(SYMBOL, level=2)
        self.assertIsInstance(book, OrderBook)
        self.assertGreater(len(book.bids) + len(book.asks), 0)

    def test_trades(self):
        trades = self.client.trades(SYMBOL)
        self.assertIsInstance(trades, list)
        if trades:
            self.assertIsInstance(trades[0], Trade)

    def test_candles(self):
        candles = self.client.candles(SYMBOL, granularity=3600)
        self.assertGreater(len(candles), 0)
        self.assertIsInstance(candles[0], Candlestick)

    def test_quotation(self):
        quoted = self.client.quotation(SYMBOL, "buy", 0.001)
        self.assertIsInstance(quoted, Quotation)
        self.assertGreater(quoted.base_exchanged, 0)


@skip_without("COINBASE_API_KEY", "COINBASE_API_SECRET", "COINBASE_PASSPHRASE")
class CoinbaseAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = Coinbase.Auth(
            env("COINBASE_API_KEY"),
            env("COINBASE_API_SECRET"),
            env("COINBASE_PASSPHRASE"),
        )

    def test_accounts(self):
        accounts = self.client.accounts()
        self.assertIsInstance(accounts, list)
