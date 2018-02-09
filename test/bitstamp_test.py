import unittest
from datetime import datetime

# pip
from decouple import config

# local
from trading_api_wrappers import errors, Bitstamp

API_KEY = config('BITSTAMP_API_KEY')
API_SECRET = config('BITSTAMP_API_SECRET')
CUSTOMER_ID = config('BITSTAMP_CUSTOMER_ID')

# Default parameters
PAIR = Bitstamp.CurrencyPair.BTC_USD
TIMESTAMP = datetime(2016, 1, 1).timestamp()

TEST_ORDERS = False  # Test orders only if explicitly set


class BitstampPublicTest(unittest.TestCase):

    def setUp(self):
        self.client = Bitstamp.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitstamp.Public)

    def test_ticker_returns_data(self):
        response = self.client.ticker(PAIR)
        self.assertIn('last', response.keys())

    def test_ticker_hour_returns_data(self):
        response = self.client.ticker_hour(PAIR)
        self.assertIn('last', response.keys())

    def test_order_book_returns_data(self):
        response = self.client.order_book(PAIR)
        self.assertIn('bids', response.keys())

    def test_transactions_returns_list(self):
        response = self.client.transactions(PAIR)
        self.assertIsInstance(response, list)

    def test_trading_pairs_info_returns_list(self):
        response = self.client.trading_pairs_info()
        self.assertIsInstance(response, list)

    def test_conversion_rate_usd_eur_returns_data(self):
        response = self.client.conversion_rate_usd_eur()
        self.assertIn('sell', response.keys())


class BitstampAuthTest(unittest.TestCase):

    def setUp(self):
        self.client = Bitstamp.Auth(API_KEY, API_SECRET, CUSTOMER_ID)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitstamp.Auth)

    def test_account_balance_returns_data(self):
        response = self.client.account_balance(PAIR)
        self.assertIn('btc_available', response.keys())

    def test_user_transactions_returns_list(self):
        response = self.client.user_transactions(PAIR)
        self.assertIsInstance(response, list)

    def test_open_orders_returns_list(self):
        response = self.client.open_orders()
        self.assertIsInstance(response, list)

    def test_orders_status_returns_order_not_found(self):
        with self.assertRaisesRegex(errors.InvalidResponse, '200'):
            self.client.orders_status(1)

    def test_cancel_order_returns_order_not_found(self):
        with self.assertRaisesRegex(errors.InvalidResponse, '200'):
            self.client.cancel_order(1)

    @unittest.skipUnless(TEST_ORDERS, 'Only run if explicitly set')
    def test_cancel_all_orders_returns_true(self):
        response = self.client.cancel_all_orders()
        self.assertTrue(response)

    # TODO: Order and withdrawal tests


class BitstampAuthTestBadApi(unittest.TestCase):

    def setUp(self):
        self.client = Bitstamp.Auth('BAD_KEY', 'BAD_SECRET', 'BAD_ID')

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitstamp.Auth)

    def test_account_balance_returns_error(self):
        self.assertRaises(errors.InvalidResponse,
                          lambda: self.client.account_balance())
