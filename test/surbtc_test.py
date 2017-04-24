import unittest

# pip
from decouple import config
from requests import RequestException

# local
from trading_api_wrappers import SURBTC
from trading_api_wrappers.surbtc import models

TEST = config('TEST', cast=bool, default=False)
API_KEY = config('SURBTC_API_KEY')
API_SECRET = config('SURBTC_API_SECRET')
MARKET_ID = SURBTC.Market.BTC_CLP


class SURBTCTest(unittest.TestCase):

    def setUp(self):
        self.client = SURBTC(API_KEY, API_SECRET, TEST)

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, SURBTC)

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

    def test_quotation(self):
        quotation = self.client.quotation(
            MARKET_ID, SURBTC.Currency.BTC,
            SURBTC.QuotationType.ASK_GIVEN_SIZE,
            price_limit=1, amount=1)
        self.assertIsInstance(quotation, models.Quotation)

    def test_fee_percentage(self):
        fee_percentage = self.client.fee_percentage(
            MARKET_ID, SURBTC.OrderType.ASK, market_order=False)
        self.assertIsInstance(fee_percentage, models.FeePercentage)

    def test_trade_transactions(self):
        trade_transactions = self.client.trade_transactions(MARKET_ID)
        for transaction in trade_transactions:
            self.assertIsInstance(transaction, models.TradeTransaction)

    # def test_reports(self):
    #     reports = self.client.reports(MARKET_ID, report_type='candlestick')
    #     self.assertIn('reports', reports.keys())

    def test_balance(self):
        balance = self.client.balance(SURBTC.Currency.BTC)
        self.assertIsInstance(balance, models.Balance)

    def test_balances_events(self):
        currencies = [item for item in SURBTC.Currency]
        event_names = [item for item in SURBTC.BalanceEvent]
        balance_events = self.client.balance_events(currencies, event_names)
        self.assertIsInstance(balance_events, models.BalanceEventPages)

    def test_orders(self):
        per_page = 10
        order_pages = self.client.orders(MARKET_ID, page=1, per_page=per_page)
        self.assertIsInstance(order_pages, models.OrderPages)
        self.assertEqual(len(order_pages.orders), per_page)

    def test_single_order(self):
        orders = self.client.orders(MARKET_ID, page=1, per_page=1).orders
        first_order = orders[0]
        single_order = self.client.single_order(first_order.id)
        self.assertIsInstance(single_order, models.Order)


class SURBTCTestBadApi(unittest.TestCase):

    def setUp(self):
        self.client = SURBTC('BAD_KEY', 'BAD_SECRET')

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, SURBTC)

    def test_key_secret(self):
        self.assertRaises(ValueError, lambda: SURBTC())

    def test_markets_returns_error(self):
        self.assertRaises(RequestException, lambda: self.client.markets())
