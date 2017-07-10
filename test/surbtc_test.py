import unittest
from datetime import datetime, timedelta

# pip
from decouple import config

# local
from trading_api_wrappers import SURBTC, errors
from trading_api_wrappers.surbtc import models

TEST = config('SURBTC_TEST', cast=bool, default=True)
API_KEY = config('SURBTC_API_KEY')
API_SECRET = config('SURBTC_API_SECRET')
MARKET_ID = SURBTC.Market.BTC_CLP


class SURBTCPublicTest(unittest.TestCase):

    def setUp(self):
        self.client = SURBTC.Public(TEST)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, SURBTC.Public)

    def test_markets(self):
        markets = self.client.markets()
        self.assertEqual(len(markets), len(SURBTC.Market))
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


class SURBTCAuthTest(unittest.TestCase):

    def setUp(self):
        self.client = SURBTC.Auth(API_KEY, API_SECRET, TEST)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, SURBTC.Auth)

    def test_quotation(self):
        quotation = self.client.quotation(
            MARKET_ID, quotation_type=SURBTC.QuotationType.ASK_GIVEN_SIZE,
            amount=1, limit=1)
        self.assertIsInstance(quotation, models.Quotation)

    def test_quotation_market(self):
        quotation = self.client.quotation(
            MARKET_ID, quotation_type=SURBTC.QuotationType.ASK_GIVEN_SIZE,
            amount=1)
        self.assertIsInstance(quotation, models.Quotation)

    def test_quotation_limit(self):
        quotation = self.client.quotation(
            MARKET_ID, quotation_type=SURBTC.QuotationType.ASK_GIVEN_SIZE,
            amount=1, limit=1)
        self.assertIsInstance(quotation, models.Quotation)

    def test_trade_transaction_pages(self):
        trade_transactions = self.client.trade_transaction_pages(MARKET_ID)
        for transaction in trade_transactions:
            self.assertIsInstance(transaction, models.TradeTransaction)

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
        balance = self.client.balance(SURBTC.Currency.BTC)
        self.assertIsInstance(balance, models.Balance)

    def test_balances_event_pages(self):
        currencies = [item for item in SURBTC.Currency]
        event_names = [item for item in SURBTC.BalanceEvent]
        balance_events = self.client.balance_event_pages(
            currencies, event_names)
        self.assertIsInstance(balance_events, models.BalanceEventPages)

    def test_withdrawals(self):
        withdrawals = self.client.withdrawals(currency=SURBTC.Currency.BTC)
        for withdrawal in withdrawals:
            self.assertIsInstance(withdrawal, models.Withdrawal)

    def test_deposits(self):
        deposits = self.client.deposits(currency=SURBTC.Currency.BTC)
        for deposit in deposits:
            self.assertIsInstance(deposit, models.Deposit)

    def test_simulate_withdrawal(self):
        simulate_withdrawal = self.client.simulate_withdrawal(
            currency=SURBTC.Currency.BTC, amount=0)
        self.assertIsInstance(simulate_withdrawal, models.Withdrawal)

    def test_order_pages(self):
        per_page = 10
        order_pages = self.client.order_pages(
            MARKET_ID, page=1, per_page=per_page)
        self.assertIsInstance(order_pages, models.OrderPages)
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
            MARKET_ID, SURBTC.OrderType.ASK, SURBTC.OrderPriceType.LIMIT,
            amount=0.001, limit=100000)
        # Cancel order
        canceled_order = self.client.cancel_order(new_order.id)
        # Assertions
        self.assertIsInstance(new_order, models.Order)
        self.assertIsInstance(canceled_order, models.Order)


class SURBTCAuthTestBadApi(unittest.TestCase):

    def setUp(self):
        self.client = SURBTC.Auth('BAD_KEY', 'BAD_SECRET')

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, SURBTC.Auth)

    def test_key_secret(self):
        self.assertRaises(ValueError,
                          lambda: SURBTC.Auth())

    def test_balance_returns_error(self):
        self.assertRaises(errors.InvalidResponse,
                          lambda: self.client.balance(SURBTC.Currency.CLP))
