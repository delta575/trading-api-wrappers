from ..base import _Enum


# API paths
class Path(object):
    PRICES = '%s/%s.json'


class Currency(_Enum):
    ARS = 'ARS'
    BRL = 'BRL'
    CLP = 'CLP'
    ETH = 'ETH'
    EUR = 'EUR'


class Market(_Enum):
    ETH_ARS = 'ethars'
    ETH_BRL = 'ethbrl'
    ETH_CLP = 'ethclp'
    ETH_EUR = 'etheur'

    @staticmethod
    def _format_value(value):
        return f'{value[:3]}_{value[3:]}'.upper()


class TimeFrame(_Enum):
    DAYS_1 = 1440
    HOURS_1 = 60
    MINUTES_15 = 15
    MINUTES_5 = 5
    MINUTES_1 = 1

    @staticmethod
    def _format_value(value):
        values = {
            1440: 'DAYS_1',
            60: 'HOURS_1',
            15: 'MINUTES_15',
            5: 'MINUTES_5',
            1: 'MINUTES_1',
        }
        return values[value]