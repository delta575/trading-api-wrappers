import unittest
from datetime import datetime

from decouple import config

from trading_api_wrappers import Bitfinex
from trading_api_wrappers import InvalidResponse

API_KEY = config("BFX_API_KEY")
API_SECRET = config("BFX_API_SECRET")

# Default parameters
SYMBOL = Bitfinex.Symbol.BTCUSD
CURRENCY = Bitfinex.Currency.BTC
TIMESTAMP = datetime(2016, 1, 1).timestamp()


class BitfinexPublicTest(unittest.TestCase):
    def setUp(self):
        self.client = Bitfinex.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitfinex.Public)

    def test_ticker_returns_data(self):
        response = self.client.ticker(SYMBOL)
        self.assertIn("last_price", response.keys())

    def test_stats_returns_data(self):
        response = self.client.stats(SYMBOL)
        self.assertIn("volume", response[0].keys())

    def test_today_returns_data(self):
        response = self.client.today(SYMBOL)
        self.assertIn("volume", response.keys())

    def test_lend_book_returns_data(self):
        response = self.client.lend_book(CURRENCY, limit_asks=1, limit_bids=1)
        self.assertIn("asks", response.keys())

    def test_order_book_returns_data(self):
        response = self.client.order_book(SYMBOL, limit_asks=1, limit_bids=1)
        self.assertIn("asks", response.keys())

    def test_trades_returns_data(self):
        response = self.client.trades(SYMBOL, TIMESTAMP, limit_trades=1)
        self.assertIn("amount", response[0].keys())

    def test_lends_returns_data(self):
        response = self.client.lends(CURRENCY, TIMESTAMP, limit_lends=1)
        self.assertIn("amount_lent", response[0].keys())

    def test_symbols_returns_data(self):
        response = self.client.symbols()
        self.assertIn(SYMBOL.value, response)

    def test_symbols_details_returns_data(self):
        response = self.client.symbols_details()
        self.assertIn("pair", response[0].keys())


class BitfinexAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = Bitfinex.Auth(API_KEY, API_SECRET)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitfinex.Auth)

    def test_account_info_returns_data(self):
        response = self.client.account_info()
        self.assertIn("maker_fees", response[0].keys())

    def test_summary_returns_data(self):
        response = self.client.summary()
        self.assertIn("maker_fee", response.keys())

    def test_key_info_returns_data(self):
        response = self.client.key_info()
        self.assertIn("account", response.keys())

    def test_margin_info_returns_data(self):
        response = self.client.margin_info()
        self.assertIn("leverage", response[0].keys())

    def test_balances_returns_data(self):
        response = self.client.balances()
        self.assertIn("amount", response[0].keys())

    def test_past_trades_returns_data(self):
        response = self.client.past_trades(SYMBOL)
        self.assertIn("amount", response[0].keys())


class BitfinexAuthTestBadApi(unittest.TestCase):
    def setUp(self):
        self.client = Bitfinex.Auth("BAD_KEY", "BAD_SECRET")

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitfinex.Auth)

    def test_key_secret(self):
        with self.assertRaises(TypeError):
            Bitfinex.Auth()

    def test_account_info_returns_error(self):
        with self.assertRaises(InvalidResponse):
            self.client.account_info()
