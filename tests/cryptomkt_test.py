import unittest

from tests.helpers import env, skip_unless_host, skip_without
from trading_api_wrappers import CryptoMKT, InvalidResponse
from trading_api_wrappers.cryptomkt import models

POST_ORDERS = False
API_KEY = env("CRYPTOMKT_API_KEY")
API_SECRET = env("CRYPTOMKT_API_SECRET")
HOST = "api.exchange.cryptomkt.com"


@skip_unless_host(HOST)
class CryptoMKTPublicTest(unittest.TestCase):
    def setUp(self):
        self.client = CryptoMKT.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CryptoMKT.Public)

    def test_markets(self):
        markets = self.client.markets()
        self.assertGreater(len(markets), 0)
        first = next(iter(markets.values()))
        self.assertIsInstance(first, models.Market)

    def test_ticker(self):
        symbol = next(iter(self.client.markets()))
        ticker = self.client.ticker(symbol)
        self.assertIsInstance(ticker, models.Ticker)
        self.assertEqual(ticker.symbol, symbol)

    def test_order_book(self):
        symbol = next(iter(self.client.markets()))
        order_book = self.client.order_book(symbol, depth=5)
        self.assertIsInstance(order_book, models.OrderBook)

    def test_trades(self):
        symbol = next(iter(self.client.markets()))
        trades = self.client.trades(symbol, limit=5)
        self.assertIsInstance(trades, list)
        if trades:
            self.assertIsInstance(trades[0], models.Trade)


@skip_unless_host(HOST)
@skip_without("CRYPTOMKT_API_KEY", "CRYPTOMKT_API_SECRET")
class CryptoMKTAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = CryptoMKT.Auth(API_KEY, API_SECRET)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CryptoMKT.Auth)

    def test_balance(self):
        balance = self.client.balance()
        self.assertIsInstance(balance, list)

    @unittest.skipUnless(POST_ORDERS, "Only run if explicitly set")
    def test_create_order_cancel_order(self):
        symbol = next(iter(self.client.markets()))
        new_order = self.client.create_order(
            symbol, CryptoMKT.OrderType.SELL, quantity=0.001, price=1000000
        )
        canceled_order = self.client.cancel_order(new_order.client_order_id)
        self.assertIsInstance(new_order, models.Order)
        self.assertIsInstance(canceled_order, models.Order)


@skip_unless_host(HOST)
class CryptoMKTAuthTestBadApi(unittest.TestCase):
    def setUp(self):
        self.client = CryptoMKT.Auth("BAD_KEY", "BAD_SECRET")

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CryptoMKT.Auth)

    def test_key_secret(self):
        with self.assertRaises(TypeError):
            CryptoMKT.Auth()

    def test_balance_returns_error(self):
        with self.assertRaises(InvalidResponse):
            self.client.balance()
