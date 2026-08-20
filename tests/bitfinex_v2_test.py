import unittest
from datetime import datetime

from tests.helpers import env, skip_without
from trading_api_wrappers import BitfinexV2 as Bitfinex
from trading_api_wrappers import InvalidResponse
from trading_api_wrappers.bitfinex import models_v2 as models

TEST = env("TEST") == "True"
API_KEY = env("BFX_API_KEY")
API_SECRET = env("BFX_API_SECRET")

# Default parameters
SYMBOL = Bitfinex.Symbol.BTCUSD
TIMESTAMP = datetime(2016, 1, 1).timestamp()


class BitfinexPublicTest(unittest.TestCase):
    def setUp(self):
        self.client = Bitfinex.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitfinex.Public)

    def test_ticker_returns_data(self):
        ticker = self.client.ticker(SYMBOL)
        self.assertIsInstance(ticker, models.TradingTicker)

    def test_tickers_returns_data(self):
        tickers = self.client.tickers([SYMBOL])
        for ticker in tickers.values():
            self.assertIsInstance(ticker, models.TradingTicker)

    def test_trades_returns_data(self):
        trades = self.client.trades(SYMBOL)
        for trade in trades:
            self.assertIsInstance(trade, models.TradingTrade)

    def test_books_returns_data(self):
        books = self.client.books(SYMBOL, Bitfinex.BookPrecision.P0)
        for book in books:
            self.assertIsInstance(book, models.TradingBook)

    def test_stats_last_returns_data(self):
        stat = self.client.stats_last(SYMBOL, key="pos.size", size="1m", side="long")
        self.assertIsInstance(stat, models.Stat)

    def test_stats_hist_returns_data(self):
        stats = self.client.stats_hist(SYMBOL, key="pos.size", size="1m", side="long")
        for stat in stats:
            self.assertIsInstance(stat, models.Stat)

    def test_candles_last_returns_data(self):
        candle = self.client.candles_last(SYMBOL, time_frame="1D")
        self.assertIsInstance(candle, models.Candle)

    def test_candles_hist_returns_data(self):
        candles = self.client.candles_hist(SYMBOL, time_frame="1D")
        for candle in candles:
            self.assertIsInstance(candle, models.Candle)


@skip_without("BFX_API_KEY", "BFX_API_SECRET")
class BitfinexAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = Bitfinex.Auth(API_KEY, API_SECRET)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitfinex.Auth)

    def test_wallets_returns_data(self):
        response = self.client.wallets()
        self.assertIsInstance(response, list)


class BitfinexAuthTestBadApi(unittest.TestCase):
    def setUp(self):
        self.client = Bitfinex.Auth("BAD_KEY", "BAD_SECRET")

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitfinex.Auth)

    def test_key_secret(self):
        with self.assertRaises(TypeError):
            Bitfinex.Auth()

    def test_wallets_returns_error(self):
        with self.assertRaises(InvalidResponse):
            self.client.wallets()
