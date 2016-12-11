import unittest
# local
from coindesk import CoinDesk

CURRENCY = 'clp'


class CoinDeskTest(unittest.TestCase):

    def setUp(self):
        self.client = CoinDesk()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CoinDesk)

    def test_current_bpi_returns_data(self):
        bpi = self.client.current_bpi(CURRENCY)
        self.assertIn('bpi', bpi.keys())

    def test_historical_bpi_returns_data(self):
        bpi = self.client.historical_bpi(currency=CURRENCY)
        self.assertIn('bpi', bpi.keys())
