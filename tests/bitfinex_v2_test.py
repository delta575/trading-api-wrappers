import unittest
from datetime import datetime

from decouple import config

from trading_api_wrappers import BitfinexV2 as Bitfinex
from trading_api_wrappers.bitfinex import models_v2 as models

TEST = config("TEST", cast=bool, default=False)
API_KEY = config("BFX_API_KEY")
API_SECRET = config("BFX_API_SECRET")

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
