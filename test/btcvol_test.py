import unittest
# local
from trading_api_wrappers import BtcVol


class BtcVolTest(unittest.TestCase):

    def setUp(self):
        self.client = BtcVol()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, BtcVol)

    def test_current_bpi_returns_data(self):
        response = self.client.latest()
        self.assertIn('Volatility', response.keys())

    def test_historical_bpi_returns_data(self):
        response = self.client.all()
        self.assertIn('Volatility', response[0].keys())
