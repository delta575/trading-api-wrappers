import unittest
from datetime import datetime, timedelta

from decouple import config

from trading_api_wrappers import Buda
from trading_api_wrappers import InvalidResponse
from trading_api_wrappers.buda import models

API_KEY = config('BUDA_API_KEY')
API_SECRET = config('BUDA_API_SECRET')
HOST = config('BUDA_HOST', default='https://www.buda.com/api/v2/')
TEST_ORDERS = config('BUDA_TEST_ORDERS', cast=bool, default=False)
MARKET_ID = Buda.Market.BTC_CLP


class BudaPublicTest(unittest.TestCase):

    def setUp(self):
        self.client = Buda.Public(base_url=HOST)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Buda.Public)

    def test_client_base_url(self):
        self.assertEqual(self.client.base_url, HOST)

    def test_markets(self):
        markets = self.client.markets()
        self.assertEqual(len(markets), len(Buda.Market))
        for market in markets:
            self.assertIsInstance(market, models.Market)

    def test_markets_details(self):
        market = self.client.market_details(MARKET_ID)
        self.assertIsInstance(market, models.Market)

    def test_ticker(self):
        ticker = self.client.ticker(MARKET_ID)
        self.assertIsInstance(ticker, models.Ticker)

    def test_order_book(self):
        order_book = self.client.order_book(MARKET_ID)
        self.assertIsInstance(order_book, models.OrderBook)

    def test_trades(self):
        timestamp = int((datetime.now() - timedelta(days=30)).timestamp())
        trades = self.client.trades(MARKET_ID, timestamp=timestamp)
        self.assertIsInstance(trades, models.Trades)
        self.assertEqual(trades.timestamp, timestamp)

    def test_report_average_prices(self):
        end = datetime.now()
        start = end - timedelta(days=30)
        report = self.client.report_average_prices(
            MARKET_ID, start_at=start, end_at=end)
        for item in report:
            self.assertIsInstance(item, models.AveragePrice)

    def test_report_candlestick(self):
        end = datetime.now()
        start = end - timedelta(days=30)
        report = self.client.report_candlestick(
            MARKET_ID, start_at=start, end_at=end)
        for item in report:
            self.assertIsInstance(item, models.Candlestick)


class BudaAuthTest(unittest.TestCase):

    def setUp(self):
        self.client = Buda.Auth(API_KEY, API_SECRET, base_url=HOST)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Buda.Auth)

    def test_client_base_url(self):
        self.assertEqual(self.client.base_url, HOST)

    def test_quotation(self):
        quotation = self.client.quotation(
            MARKET_ID, quotation_type=Buda.QuotationType.ASK_GIVEN_SIZE,
            amount=1, limit=1)
        self.assertIsInstance(quotation, models.Quotation)

    def test_quotation_market(self):
        quotation = self.client.quotation(
            MARKET_ID, quotation_type=Buda.QuotationType.ASK_GIVEN_SIZE,
            amount=1)
        self.assertIsInstance(quotation, models.Quotation)

    def test_quotation_limit(self):
        quotation = self.client.quotation(
            MARKET_ID, quotation_type=Buda.QuotationType.ASK_GIVEN_SIZE,
            amount=1, limit=1)
        self.assertIsInstance(quotation, models.Quotation)

    def test_balance(self):
        balance = self.client.balance(Buda.Currency.BTC)
        self.assertIsInstance(balance, models.Balance)

    @unittest.skip('Takes longer than timeout')
    def test_balances_event_pages(self):
        currencies = [item for item in Buda.Currency]
        event_names = [item for item in Buda.BalanceEvent]
        balance_events = self.client.balance_event_pages(
            currencies, event_names)
        self.assertIsInstance(balance_events, models.BalanceEventPages)

    def test_withdrawal_pages(self):
        page, per_page = 2, 10
        withdrawal_pages = self.client.withdrawal_pages(
            Buda.Currency.BTC, page=page, per_page=per_page)
        self.assertIsInstance(withdrawal_pages, models.WithdrawalPages)
        self.assertEqual(withdrawal_pages.meta.current_page, page)
        self.assertEqual(len(withdrawal_pages.withdrawals), per_page)

    def test_withdrawals(self):
        withdrawals = self.client.withdrawals(currency=Buda.Currency.BTC)
        for withdrawal in withdrawals:
            self.assertIsInstance(withdrawal, models.Withdrawal)

    def test_deposit_pages(self):
        page, per_page = 2, 10
        deposit_pages = self.client.deposit_pages(
            Buda.Currency.BTC, page=page, per_page=per_page)
        self.assertIsInstance(deposit_pages, models.DepositPages)
        self.assertEqual(deposit_pages.meta.current_page, page)
        self.assertEqual(len(deposit_pages.deposits), per_page)

    def test_deposits(self):
        deposits = self.client.deposits(currency=Buda.Currency.BTC)
        for deposit in deposits:
            self.assertIsInstance(deposit, models.Deposit)

    def test_simulate_withdrawal(self):
        simulate_withdrawal = self.client.simulate_withdrawal(
            currency=Buda.Currency.BTC, amount=0)
        self.assertIsInstance(simulate_withdrawal, models.Withdrawal)

    def test_order_pages(self):
        page, per_page = 2, 10
        order_pages = self.client.order_pages(
            MARKET_ID, page=page, per_page=per_page)
        self.assertIsInstance(order_pages, models.OrderPages)
        self.assertEqual(order_pages.meta.current_page, page)
        self.assertEqual(len(order_pages.orders), per_page)

    def test_order_details(self):
        orders = self.client.order_pages(
            MARKET_ID, page=1, per_page=1).orders
        first_order = orders[0]
        single_order = self.client.order_details(first_order.id)
        self.assertIsInstance(single_order, models.Order)

    @unittest.skipUnless(TEST_ORDERS, 'Only run on staging context')
    def test_new_order_cancel_order(self):
        # New order
        new_order = self.client.new_order(
            MARKET_ID, Buda.OrderType.ASK, Buda.OrderPriceType.LIMIT,
            amount=0.001, limit=100000)
        # Cancel order
        canceled_order = self.client.cancel_order(new_order.id)
        # Assertions
        self.assertIsInstance(new_order, models.Order)
        self.assertIsInstance(canceled_order, models.Order)


class BudaAuthTestBadApi(unittest.TestCase):

    def setUp(self):
        self.client = Buda.Auth('BAD_KEY', 'BAD_SECRET', base_url=HOST)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Buda.Auth)

    def test_client_base_url(self):
        self.assertEqual(self.client.base_url, HOST)

    def test_key_secret(self):
        with self.assertRaises(TypeError):
            Buda.Auth()

    def test_balance_returns_error(self):
        with self.assertRaises(InvalidResponse):
            self.client.balance(Buda.Currency.CLP)
