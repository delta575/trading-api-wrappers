import unittest
from decouple import config

from surbtc import SURBTC

TEST = config('TEST', cast=bool, default=False)
API_KEY = config('API_KEY')
API_SECRET = config('API_SECRET')
MARKET_ID = 'btc-clp'


class SURBTCTest(unittest.TestCase):

    def setUp(self):
        self.client = SURBTC(API_KEY, API_SECRET, TEST)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, SURBTC)

    def test_markets_returns_data(self):
        markets = self.client.markets()
        self.assertIn('markets', markets.keys())

    def test_markets_details_returns_data(self):
        markets_details = self.client.market_details(MARKET_ID)
        self.assertIn('market', markets_details.keys())

    def test_indicators_returns_data(self):
        indicators = self.client.indicators(MARKET_ID)
        self.assertIn('indicators', indicators.keys())

    def test_order_book_returns_data(self):
        order_book = self.client.order_book(MARKET_ID)
        self.assertIn('order_book', order_book.keys())

    def test_quotation_returns_data(self):
        quotation = self.client.quotation(
            MARKET_ID, quotation_type='ask', reverse=False, amount=1)
        self.assertIn('quotation', quotation.keys())

    def test_fee_percentage_returns_data(self):
        fee_percentage = self.client.fee_percentage(
            MARKET_ID, order_type='Bid', market_order=False)
        self.assertIn('fee_percentage', fee_percentage.keys())

    def test_trade_transactions_returns_data(self):
        trade_transactions = self.client.trade_transactions(MARKET_ID)
        self.assertIn('trade_transactions', trade_transactions.keys())

    def test_reports_returns_data(self):
        reports = self.client.reports(MARKET_ID, report_type='candlestick')
        self.assertIn('reports', reports.keys())

    def test_balance_returns_data(self):
        balance = self.client.balance(currency='BTC')
        self.assertIn('balance', balance.keys())

    def test_balances_events_returns_data(self):
        currencies = ['BTC', 'CLP']
        event_names = [
            'deposit_confirm',
            'withdrawal_confirm',
            'transaction',
            'transfer_confirmation',
        ]
        balance_events = self.client.balance_events(currencies, event_names)
        self.assertIn('balance_events', balance_events.keys())

    def test_orders_returns_data(self):
        per_page = 10
        orders = self.client.orders(MARKET_ID, page=1, per_page=per_page)
        self.assertIn('orders', orders.keys())
        self.assertEqual(len(orders['orders']), per_page)

    def test_single_order_returns_data(self):
        first_order = self.client.orders(MARKET_ID, page=1, per_page=1)['orders'][0]
        single_order = self.client.single_order(first_order['id'])
        self.assertIn('order', single_order.keys())


class SURBTCTestBadApi(unittest.TestCase):

    def setUp(self):
        self.client = SURBTC('BAD_KEY', 'BAD_SECRET')

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, SURBTC)

    def test_key_secret(self):
        self.assertRaises(ValueError, lambda: SURBTC())

    def test_markets_returns_error(self):
        self.assertRaises(Exception, lambda: self.client.markets())
