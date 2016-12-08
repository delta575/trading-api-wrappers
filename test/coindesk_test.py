import unittest

from coindesk import CoinDesk

CURRENCY = 'clp'


class CoinDeskTest(unittest.TestCase):

    def setUp(self):
        self.client = CoinDesk()

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CoinDesk)

    def test_getBPI_returns_data(self):
        bpi = self.client.getBPI(CURRENCY)
        self.assertIn('bpi', bpi.keys())
