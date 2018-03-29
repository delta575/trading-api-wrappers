# local
import unittest

# pip
from decouple import config

# local
from trading_api_wrappers import CurrencyLayer
from trading_api_wrappers.errors import InvalidResponse

ACCESS_KEY = config('CURRENCYLAYER_ACCESS_KEY')

# TODO: Improve tests with a paid plan


class CurrencyLayerTest(unittest.TestCase):

    def setUp(self):
        self.client = CurrencyLayer(ACCESS_KEY)

    def skip_test_non_paid_plan(self, exception):
        if 'Access Restricted' in exception.message:
            raise self.skipTest('PAID PLAN REQUIRED')

    def test_instantiate_client(self):
        self.assertIsInstance(self.client, CurrencyLayer)

    def test_currencies(self):
        currencies = self.client.currencies()
        self.assertIn('currencies', currencies)
        self.assertIn('EUR', currencies['currencies'])
        self.assertIn('CLP', currencies['currencies'])
        self.assertEqual('Euro', currencies['currencies']['EUR'])
        self.assertEqual('Chilean Peso', currencies['currencies']['CLP'])

    def test_live_rates(self):
        rates = self.client.live_rates()
        self.assertEqual('USD', rates['source'])
        self.assertIn('USDEUR', rates['quotes'])
        self.assertIn('USDCLP', rates['quotes'])
        self.assertIn('timestamp', rates)

    def test_get_live_rates_for_base(self):
        try:
            rates = self.client.live_rates(base='EUR')
        except InvalidResponse as e:
            raise self.skip_test_non_paid_plan(e)
        self.assertEqual('EUR', rates['source'])
        self.assertIn('USDEUR', rates['quotes'])
        self.assertIn('CLPEUR', rates['quotes'])
        self.assertIn('timestamp', rates)

    def test_get_live_rates_for_currencies(self):
        rates_for = self.client.live_rates(currencies=['USD', 'EUR'])
        self.assertIn('quotes', rates_for)
        self.assertEqual('USD', rates_for['source'])
        self.assertIn('USDUSD', rates_for['quotes'])
        self.assertIn('USDEUR', rates_for['quotes'])
        self.assertEqual(2, len(rates_for['quotes']))

    def test_historical(self):
        historical = self.client.historical('2010-01-01')
        self.assertEqual(True, historical['historical'])
        self.assertEqual('2010-01-01', historical['date'])
        self.assertEqual('USD', historical['source'])
        self.assertEqual(1, historical['quotes']['USDUSD'])
        self.assertEqual(0.697253, historical['quotes']['USDEUR'])

    def test_historical_for_base(self):
        try:
            historical = self.client.historical('2010-01-01', base='EUR')
        except InvalidResponse as e:
            return self.skip_test_non_paid_plan(e)
        self.assertEqual(True, historical['historical'])
        self.assertEqual('2010-01-01', historical['date'])
        self.assertEqual('EUR', historical['source'])
        self.assertEqual(1, historical['quotes']['EUREUR'])
        # self.assertEqual(?, historical['quotes']['2010-01-01']['EURUSD'])

    def test_convert(self):
        try:
            convert_rate = self.client.convert(10, 'USD', 'EUR')
        except InvalidResponse as e:
            raise self.skip_test_non_paid_plan(e)
        self.assertEqual('USD', convert_rate['query']['from'])
        self.assertEqual('EUR', convert_rate['query']['to'])
        self.assertEqual(10, convert_rate['query']['amount'])
        # self.assertEqual(?, convert_rate['result'])

    def test_convert_for_date(self):
        try:
            convert_rate = self.client.convert(10, 'USD', 'EUR', '2010-01-01')
        except InvalidResponse as e:
            raise self.skip_test_non_paid_plan(e)
        self.assertEqual('USD', convert_rate['query']['from'])
        self.assertEqual('EUR', convert_rate['query']['to'])
        self.assertEqual('2010-01-01', convert_rate['date'])
        self.assertEqual(10, convert_rate['query']['amount'])
        # self.assertEqual(?, convert_rate['result'])

    def test_time_frame(self):
        try:
            time_frame = self.client.time_frame(
                '2012-01-01', '2012-02-29',
                currencies=['USD', 'EUR'])
        except InvalidResponse as e:
            raise self.skip_test_non_paid_plan(e)
        self.assertEqual('USD', time_frame['source'])
        self.assertEqual('2012-01-01', time_frame['start_date'])
        self.assertEqual('2012-02-29', time_frame['end_date'])
        self.assertEqual(60, len(time_frame['quotes']))
        self.assertEqual(1, time_frame['quotes']['2010-01-01']['USDUSD'])
        self.assertEqual(0.697253, time_frame['quotes']['2010-01-01']['USDEUR'])

    def test_time_frame_for_base(self):
        try:
            time_frame = self.client.time_frame(
                '2012-01-01', '2012-03-01',
                currencies=['USD', 'EUR'],
                base='EUR')
        except InvalidResponse as e:
            raise self.skip_test_non_paid_plan(e)
        self.assertEqual('EUR', time_frame['source'])
        self.assertEqual('2012-01-01', time_frame['start_date'])
        self.assertEqual('2012-02-29', time_frame['end_date'])
        self.assertEqual(60, len(time_frame['quotes']))
        self.assertEqual(1, time_frame['quotes']['2010-01-01']['EUREUR'])
        # self.assertEqual(?, time_frame['quotes']['2010-01-01']['EURUSD'])

    def test_change(self):
        try:
            time_frame = self.client.change(currencies=['USD', 'EUR'])
        except InvalidResponse as e:
            raise self.skip_test_non_paid_plan(e)
        self.assertIn('quotes', time_frame)
        self.assertEqual('USD', time_frame['source'])
        self.assertIn('USDUSD', time_frame['quotes'])
        self.assertIn('USDEUR', time_frame['quotes'])
        self.assertEqual(2, len(time_frame['quotes']))

    def test_change_time_frame(self):
        try:
            time_frame = self.client.change_time_frame(
                '2005-01-01', '2010-01-01',
                currencies=['GBP', 'EUR'])
        except InvalidResponse as e:
            raise self.skip_test_non_paid_plan(e)

        self.assertEqual('USD', time_frame['source'])
        self.assertEqual('2005-01-01', time_frame['start_date'])
        self.assertEqual('2010-01-01', time_frame['end_date'])

        self.assertEqual(0.51961, time_frame['quotes']['USDGBP']['start_rate'])
        self.assertEqual(0.618228, time_frame['quotes']['USDGBP']['end_rate'])
        self.assertEqual(0.0986, time_frame['quotes']['USDGBP']['change'])
        self.assertEqual(18.9792, time_frame['quotes']['USDGBP']['change_pct'])

        self.assertEqual(0.73618, time_frame['quotes']['USDEUR']['start_rate'])
