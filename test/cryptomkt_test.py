import unittest
from datetime import datetime, timedelta

# pip
from decouple import config

# local
from trading_api_wrappers import CryptoMKT, errors
from trading_api_wrappers.cryptomkt import models

POST_ORDERS = False  # Only post orders if explicitly set

API_KEY = config('CRYPTOMKT_API_KEY')
API_SECRET = config('CRYPTOMKT_API_SECRET')
MARKET_ID = CryptoMKT.Market.ETH_CLP
CURRENCY = CryptoMKT.Currency.ETH


class CryptoMKTPublicTest(unittest.TestCase):

    def setUp(self):
        self.client = CryptoMKT.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CryptoMKT.Public)

    def test_markets(self):
        markets = self.client.markets()
        self.assertEqual(len(markets), len(CryptoMKT.Market))

    def test_ticker(self):
        ticker = self.client.ticker(MARKET_ID)
        self.assertIsInstance(ticker, models.Ticker)

    def test_order_book(self):
        order_book = self.client.order_book(
            MARKET_ID, CryptoMKT.OrderType.BUY)
        self.assertIsInstance(order_book, models.OrderBook)

    def test_trades(self):
        page, limit = 2, 10
        trades = self.client.trades(MARKET_ID, page=page, limit=limit)
        self.assertIsInstance(trades, models.Trades)
        self.assertEqual(trades.pagination.page, page)
        self.assertEqual(len(trades.trades), limit)

    def test_trades_dates(self):
        end = datetime.now() - timedelta(days=1)
        trades = self.client.trades(MARKET_ID, end=end)
        self.assertIsInstance(trades, models.Trades)
        self.assertLess(trades.trades[0].timestamp, end)


class CryptoMKTAuthTest(unittest.TestCase):

    def setUp(self):
        self.client = CryptoMKT.Auth(API_KEY, API_SECRET)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CryptoMKT.Auth)

    def test_balance(self):
        balance = self.client.balance()
        self.assertIsInstance(balance, models.Balance)

    def test_wallet_balance(self):
        wallet_balance = self.client.wallet_balance(CURRENCY)
        self.assertIsInstance(wallet_balance, models.WalletBalance)
        self.assertEquals(wallet_balance.wallet, CURRENCY.value)

    def test_active_orders(self):
        page, limit = 2, 10
        active_orders = self.client.active_orders(
            MARKET_ID, page=page, limit=limit)
        self.assertIsInstance(active_orders, models.Orders)
        if active_orders.orders:
            self.assertEqual(active_orders.pagination.page, page)

    def test_executed_orders(self):
        page, limit = 2, 10
        executed_orders = self.client.executed_orders(
            MARKET_ID, page=page, limit=limit)
        self.assertIsInstance(executed_orders, models.Orders)
        if executed_orders.orders:
            self.assertEqual(executed_orders.pagination.page, page)
            self.assertEqual(len(executed_orders.orders), limit)

    def test_order_status(self):
        orders = self.client.executed_orders(
            MARKET_ID, page=1, limit=1).orders
        first_order = orders[0]
        single_order = self.client.order_status(first_order.id)
        self.assertIsInstance(single_order, models.Order)

    @unittest.skipUnless(POST_ORDERS, 'Only run if explicitly set')
    def test_create_order_cancel_order(self):
        # New order
        new_order = self.client.create_order(
            MARKET_ID, CryptoMKT.OrderType.SELL,
            amount=0.001, price=1000000)
        # Cancel order
        canceled_order = self.client.cancel_order(new_order.id)
        # Assertions
        self.assertIsInstance(new_order, models.Order)
        self.assertIsInstance(canceled_order, models.Order)


class CRYPTOMKTAuthTestBadApi(unittest.TestCase):

    def setUp(self):
        self.client = CryptoMKT.Auth('BAD_KEY', 'BAD_SECRET')

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CryptoMKT.Auth)

    def test_key_secret(self):
        self.assertRaises(ValueError, lambda: CryptoMKT.Auth())

    def test_balance_returns_error(self):
        self.assertRaises(errors.InvalidResponse,
                          lambda: self.client.balance())
