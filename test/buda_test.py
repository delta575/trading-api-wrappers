import unittest
from datetime import datetime, timedelta

# pip
from decouple import config

# local
from trading_api_wrappers import Buda, errors
from trading_api_wrappers.buda import models

TEST = config('BUDA_TEST', cast=bool, default=True)
API_KEY = config('BUDA_API_KEY')
API_SECRET = config('BUDA_API_SECRET')
MARKET_ID = Buda.Market.BTC_CLP


class BudaPublicTest(unittest.TestCase):

    def setUp(self):
        self.client = Buda.Public(TEST)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Buda.Public)

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

    def test_trade_transaction_pages(self):
        page, per_page = 2, 10
        trade_trans_pages = self.client.trade_transaction_pages(
            MARKET_ID, page=page, per_page=per_page)
        self.assertIsInstance(trade_trans_pages, models.TradeTransactionPages)
        self.assertEqual(trade_trans_pages.meta.current_page, page)
        self.assertEqual(len(trade_trans_pages.trade_transactions), per_page)


class BudaAuthTest(unittest.TestCase):

    def setUp(self):
        self.client = Buda.Auth(API_KEY, API_SECRET, TEST)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Buda.Auth)

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

    def test_balance(self):
        balance = self.client.balance(Buda.Currency.BTC)
        self.assertIsInstance(balance, models.Balance)

    def test_balances_event_pages(self):
        currencies = [item for item in Buda.Currency]
        event_names = [item for item in Buda.BalanceEvent]
        balance_events = self.client.balance_event_pages(
            currencies, event_names)
        self.assertIsInstance(balance_events, models.BalanceEventPages)

    def test_withdrawals(self):
        withdrawals = self.client.withdrawals(currency=Buda.Currency.BTC)
        for withdrawal in withdrawals:
            self.assertIsInstance(withdrawal, models.Withdrawal)

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

    @unittest.skipUnless(TEST, 'Only run on staging context')
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
        self.client = Buda.Auth('BAD_KEY', 'BAD_SECRET')

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Buda.Auth)

    def test_key_secret(self):
        self.assertRaises(ValueError,
                          lambda: Buda.Auth())

    def test_balance_returns_error(self):
        self.assertRaises(errors.InvalidResponse,
                          lambda: self.client.balance(Buda.Currency.CLP))
