import unittest

from trading_api_wrappers.market import OrderBook, OrderBookEntry, quote_from_book


class QuoteFromBookTest(unittest.TestCase):
    def setUp(self):
        self.book = OrderBook(
            bids=[
                OrderBookEntry(100, 1),
                OrderBookEntry(99, 2),
            ],
            asks=[
                OrderBookEntry(101, 1),
                OrderBookEntry(102, 2),
            ],
            timestamp=None,
            json={},
        )

    def test_buy_given_size(self):
        quoted = quote_from_book(self.book, "bid_given_size", 1.5)
        self.assertEqual(quoted.side, "buy")
        self.assertEqual(quoted.base_exchanged, 1.5)
        self.assertEqual(quoted.quote_exchanged, 101 * 1 + 102 * 0.5)
        self.assertFalse(quoted.incomplete)

    def test_sell_given_size(self):
        quoted = quote_from_book(self.book, "ask_given_size", 2)
        self.assertEqual(quoted.side, "sell")
        self.assertEqual(quoted.base_exchanged, 2)
        self.assertEqual(quoted.quote_exchanged, 100 * 1 + 99 * 1)
        self.assertFalse(quoted.incomplete)

    def test_buy_spent_quote(self):
        quoted = quote_from_book(self.book, "bid_given_spent_quote", 101)
        self.assertEqual(quoted.base_exchanged, 1)
        self.assertFalse(quoted.incomplete)

    def test_incomplete_when_book_too_thin(self):
        quoted = quote_from_book(self.book, "buy", 10)
        self.assertTrue(quoted.incomplete)
        self.assertEqual(quoted.base_exchanged, 3)

    def test_kraken_result_envelope(self):
        data = {
            "error": [],
            "result": {
                "XXBTZUSD": {
                    "bids": [["100", "1", "123"]],
                    "asks": [["101", "2", "123"]],
                }
            },
        }
        book = OrderBook.create(data)
        quoted = quote_from_book(book, "bid_given_size", 1)
        self.assertEqual(quoted.base_exchanged, 1)
        self.assertEqual(quoted.quote_exchanged, 101)
