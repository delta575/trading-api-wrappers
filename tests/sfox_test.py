import unittest

from trading_api_wrappers import SFOX
from trading_api_wrappers.sfox import models


class SFOXPublicTest(unittest.TestCase):

    def setUp(self):
        self.client = SFOX.Public()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, SFOX.Public)

    def test_best_buy_price(self):
        price = self.client.best_buy_price(1.0)
        self.assertIsInstance(price, models.Price)

    def test_best_sell_price(self):
        price = self.client.best_sell_price(1.0)
        self.assertIsInstance(price, models.Price)

    def test_order_book_raw(self):
        order_book = self.client.order_book_raw()
        self.assertEqual(
            sorted(['asks', 'bids', 'currency', 'exchanges', 'lastupdated',
                    'market_making', 'pair']),
            sorted(list(order_book.keys())))

    def test_order_book(self):
        order_book = self.client.order_book()
        self.assertIsInstance(order_book, models.OrderBook)

    def test_market_making_order_book(self):
        order_book = self.client.market_making_order_book()
        self.assertIsInstance(order_book, models.OrderBook)
