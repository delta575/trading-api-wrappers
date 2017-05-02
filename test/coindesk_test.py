import unittest
from datetime import datetime, timedelta

# local
from trading_api_wrappers import CoinDesk

CURRENCY = 'clp'
TODAY = datetime.utcnow().date()
YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)


class CoinDeskTest(unittest.TestCase):

    def setUp(self):
        self.client = CoinDesk()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CoinDesk)

    def test_bpi_current_returns_data(self):
        bpi = self.client.bpi(CURRENCY).current()
        self.assertIn('bpi', bpi.keys())

    def test_historical_bpi_returns_data(self):
        bpi = self.client.bpi(currency=CURRENCY).historical(YESTERDAY, TODAY)
        self.assertIn('bpi', bpi.keys())

    def test_rate_current_returns_float(self):
        rate = self.client.rate(CURRENCY).current()
        self.assertIsInstance(rate, float)

    def test_rate_historical_returns_valid_dict(self):
        rate_dict = self.client.rate(CURRENCY).historical(YESTERDAY, TODAY)
        self.assertIn(str(YESTERDAY), rate_dict.keys())
        self.assertNotIn(str(TODAY), rate_dict.keys())
        self.assertEqual(len(rate_dict), 1)

    def test_rate_for_date_today_returns_float(self):
        rate = self.client.rate(CURRENCY).for_date(TODAY)
        self.assertIsInstance(rate, float)

    def test_rate_for_date_yesterday_returns_float(self):
        rate = self.client.rate(CURRENCY).for_date(YESTERDAY)
        self.assertIsInstance(rate, float)

    def test_rate_for_date_tomorrow_raises_error(self):
        self.assertRaises(ValueError, lambda:
                          self.client.rate(CURRENCY).for_date(TOMORROW))
