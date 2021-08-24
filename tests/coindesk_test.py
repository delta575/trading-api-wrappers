import unittest
from datetime import datetime, timedelta

from trading_api_wrappers import CoinDesk

CURRENCY = "clp"
TODAY = datetime.utcnow()
YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)
LAST_WEEK = TODAY - timedelta(days=7)


class CoinDeskTest(unittest.TestCase):
    def setUp(self):
        self.client = CoinDesk()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CoinDesk)

    # Test BPI ----------------------------------------------------------------
    def test_bpi_current_returns_data(self):
        bpi = self.client.bpi(CURRENCY).current()
        self.assertIn("bpi", bpi.keys())

    def test_historical_bpi_returns_data(self):
        bpi = self.client.bpi(currency=CURRENCY).historical(YESTERDAY, TODAY)
        self.assertIn("bpi", bpi.keys())

    # Test Rate ---------------------------------------------------------------
    # Current
    def test_rate_current_returns_float(self):
        rate = self.client.rate(CURRENCY).current()
        self.assertIsInstance(rate, float)

    # Historical
    def test_rate_historical_yesterday_today(self):
        rate_dict = self.client.rate(CURRENCY).historical(
            YESTERDAY, TODAY, include_today=True
        )
        self.assertIn(str(YESTERDAY.date()), rate_dict.keys())
        self.assertIn(str(TODAY.date()), rate_dict.keys())
        self.assertEqual(len(rate_dict), 2)

    def test_rate_historical_last_week(self):
        rate_dict = self.client.rate(CURRENCY).historical(LAST_WEEK)
        self.assertIn(str(LAST_WEEK.date()), rate_dict.keys())
        self.assertIn(str(YESTERDAY.date()), rate_dict.keys())
        self.assertNotIn(str(TODAY.date()), rate_dict.keys())
        self.assertEqual(len(rate_dict), 7)

    def test_rate_historical_end_raises_error(self):
        self.assertRaises(
            AssertionError,
            lambda: self.client.rate(CURRENCY).historical(YESTERDAY, TOMORROW),
        )

    def test_rate_historical_start_raises_error(self):
        self.assertRaises(
            AssertionError,
            lambda: self.client.rate(CURRENCY).historical(TOMORROW, TOMORROW),
        )

    def test_rate_historical_inverted_raises_error(self):
        self.assertRaises(
            AssertionError,
            lambda: self.client.rate(CURRENCY).historical(TODAY, LAST_WEEK),
        )

    # For date
    def test_rate_for_date_today(self):
        rate = self.client.rate(CURRENCY).for_date(TODAY)
        self.assertIsInstance(rate, float)

    def test_rate_for_date_yesterday_raises_error(self):
        rate = self.client.rate(CURRENCY).for_date(YESTERDAY)
        self.assertIsInstance(rate, float)

    def test_rate_for_date_last_Week_raises_error(self):
        rate = self.client.rate(CURRENCY).for_date(LAST_WEEK)
        self.assertIsInstance(rate, float)

    def test_rate_for_date_tomorrow_raises_error(self):
        self.assertRaises(
            AssertionError, lambda: self.client.rate(CURRENCY).for_date(TOMORROW)
        )

    # Date since
    def test_rate_date_since_today(self):
        rate_dict = self.client.rate(CURRENCY).since_date(TODAY)
        self.assertIn(str(TODAY.date()), rate_dict.keys())
        self.assertEqual(len(rate_dict), 1)

    def test_rate_date_since_yesterday(self):
        rate_dict = self.client.rate(CURRENCY).since_date(YESTERDAY, include_today=True)
        self.assertIn(str(YESTERDAY.date()), rate_dict.keys())
        self.assertIn(str(TODAY.date()), rate_dict.keys())
        self.assertEqual(len(rate_dict), 2)

    def test_rate_date_since_last_week(self):
        rate_dict = self.client.rate(CURRENCY).since_date(LAST_WEEK)
        self.assertIn(str(LAST_WEEK.date()), rate_dict.keys())
        self.assertIn(str(YESTERDAY.date()), rate_dict.keys())
        self.assertNotIn(str(TODAY.date()), rate_dict.keys())
        self.assertEqual(len(rate_dict), 7)

    def test_rate_date_since_tomorrow_raises_error(self):
        self.assertRaises(
            AssertionError, lambda: self.client.rate(CURRENCY).since_date(TOMORROW)
        )

    # Date since
    def test_rate_last_n_days_0(self):
        rate_dict = self.client.rate(CURRENCY).last_n_days(0)
        self.assertIn(str(TODAY.date()), rate_dict.keys())
        self.assertEqual(len(rate_dict), 1)

    def test_rate_last_n_days_1(self):
        rate_dict = self.client.rate(CURRENCY).last_n_days(1, include_today=True)
        self.assertIn(str(YESTERDAY.date()), rate_dict.keys())
        self.assertIn(str(TODAY.date()), rate_dict.keys())
        self.assertEqual(len(rate_dict), 2)

    def test_rate_last_n_days_7(self):
        rate_dict = self.client.rate(CURRENCY).last_n_days(7)
        self.assertIn(str(LAST_WEEK.date()), rate_dict.keys())
        self.assertIn(str(YESTERDAY.date()), rate_dict.keys())
        self.assertNotIn(str(TODAY.date()), rate_dict.keys())
        self.assertEqual(len(rate_dict), 7)

    def test_rate_last_n_days_future_raises_error(self):
        self.assertRaises(
            AssertionError, lambda: self.client.rate(CURRENCY).last_n_days(-1)
        )
