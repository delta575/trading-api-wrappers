import unittest

from trading_api_wrappers import Bitex
from trading_api_wrappers.bitex import models

MARKET_ID = "btc_usd"


class BitexPublicTest(unittest.TestCase):
    def setUp(self):
        self.client = Bitex.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, Bitex.Public)

    def test_ticker(self):
        ticker = self.client.ticker(MARKET_ID)
        self.assertIsInstance(ticker, models.Ticker)

    def test_order_book(self):
        order_book = self.client.order_book(MARKET_ID)
        self.assertIsInstance(order_book, models.OrderBook)

    def test_transactions(self):
        transactions = self.client.transactions(MARKET_ID)
        for tx in transactions:
            self.assertIsInstance(tx, models.Transaction)

    @unittest.skip("Large download")
    def test_transactions_archive(self):
        transactions = self.client.transactions_archive(MARKET_ID)
        for tx in transactions:
            self.assertIsInstance(tx, models.Transaction)
