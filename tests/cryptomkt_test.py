import unittest
import warnings

from tests.helpers import skip_without
from trading_api_wrappers import CryptoMKT, NotBank
from trading_api_wrappers.market import OrderBook, Ticker


class CryptoMKTAliasTest(unittest.TestCase):
    def test_public_is_notbank_subclass(self):
        self.assertTrue(issubclass(CryptoMKT.Public, NotBank.Public))

    def test_auth_is_notbank_subclass(self):
        self.assertTrue(issubclass(CryptoMKT.Auth, NotBank.Auth))

    def test_public_warns(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            CryptoMKT.Public()
        self.assertTrue(any(item.category is DeprecationWarning for item in caught))


class CryptoMKTPublicTest(unittest.TestCase):
    def setUp(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            self.client = CryptoMKT.Public()

    def test_ticker(self):
        ticker = self.client.ticker("BTCCLP")
        self.assertIsInstance(ticker, Ticker)
        self.assertTrue(ticker.last or ticker.bid or ticker.ask)

    def test_order_book(self):
        book = self.client.order_book("BTCCLP", depth=5)
        self.assertIsInstance(book, OrderBook)
        self.assertGreater(len(book.bids) + len(book.asks), 0)


@skip_without("CRYPTOMKT_API_KEY", "CRYPTOMKT_API_SECRET", "CRYPTOMKT_USER_ID")
class CryptoMKTAuthTest(unittest.TestCase):
    def setUp(self):
        from tests.helpers import env

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            self.client = CryptoMKT.Auth(
                env("CRYPTOMKT_API_KEY"),
                env("CRYPTOMKT_API_SECRET"),
                env("CRYPTOMKT_USER_ID"),
            )

    def test_balances(self):
        balances = self.client.balances()
        self.assertIsNotNone(balances)
