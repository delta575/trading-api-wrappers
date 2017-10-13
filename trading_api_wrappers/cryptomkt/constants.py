from ..base import _Enum


# API paths
class Path(object):
    MARKETS = 'market'
    TICKER = "ticker"
    ORDER_BOOK = 'book'
    TRADES = 'trades'
    ORDERS = 'orders'
    ACTIVE_ORDER = 'orders/active'
    EXCECUTED_ORDERS = 'orders/executed'
    NEW_ORDER = 'orders/create'
    ORDER_STATUS = 'orders/status'
    CANCEL_ORDER = 'orders/cancel'
    BALANCE = 'balance'


class Currency(_Enum):
    ARS = 'ARS'
    BRL = 'BRL'
    CLP = 'CLP'
    ETH = 'ETH'
    EUR = 'EUR'

class OrderBook(_Enum):
    BUY = 'buy'
    SELL = 'sell'


class Market(_Enum):
    ETH_ARS = 'ethars'
    ETH_BRL = 'ethbrl'
    ETH_CLP = 'ethclp'
    ETH_EUR = 'etheur'

    @staticmethod
    def _format_value(value):
        return '{0}_{1}'.format(value[:3], value[3:]).upper()


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