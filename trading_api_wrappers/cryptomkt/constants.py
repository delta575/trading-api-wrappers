from ..base import _Enum, _Market, _Currency

# Limits
ORDERS_LIMIT = 100


# API paths
class Path(object):
    MARKETS = 'market'
    TICKER = 'ticker'
    ORDER_BOOK = 'book'
    TRADES = 'trades'
    ORDERS = 'orders'
    ACTIVE_ORDERS = 'orders/active'
    EXECUTED_ORDERS = 'orders/executed'
    CREATE_ORDER = 'orders/create'
    ORDER_STATUS = 'orders/status'
    CANCEL_ORDER = 'orders/cancel'
    BALANCE = 'balance'
    CREATE_PAYMENT = 'payment/new_order'
    PAYMENT_STATUS = 'payment/status'


class Currency(_Currency):
    ARS = dict(value='ARS')
    BRL = dict(value='BRL')
    CLP = dict(value='CLP')
    ETH = dict(value='ETH', decimals=18)
    EUR = dict(value='EUR')


class OrderType(_Enum):
    BUY = 'buy'
    SELL = 'sell'


class Market(_Market):
    ETH_ARS = dict(value='ETHARS', base=Currency.ETH, quote=Currency.ARS)
    ETH_CLP = dict(value='ETHCLP', base=Currency.ETH, quote=Currency.CLP)
    ETH_EUR = dict(value='ETHEUR', base=Currency.ETH, quote=Currency.EUR)


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
