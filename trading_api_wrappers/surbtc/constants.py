from enum import Enum

# Limits
ORDERS_LIMIT = 300


# API paths
class Path(object):
    MARKETS = 'markets'
    MARKET_DETAILS = 'markets/%s'
    TICKER = "markets/%s/ticker"
    ORDER_BOOK = 'markets/%s/order_book'
    QUOTATION = 'markets/%s/quotations'
    FEE_PERCENTAGE = 'markets/%s/fee_percentage'
    TRADE_TRANSACTIONS = 'markets/%s/trade_transactions'
    REPORTS = 'markets/%s/reports'
    BALANCES = 'balances/%s'
    BALANCES_EVENTS = 'balance_events'
    ORDERS = 'markets/%s/orders'
    SINGLE_ORDER = 'orders/%s'
    WITHDRAWAL = 'currencies/%s/withdrawals'


class _Enum(Enum):

    @staticmethod
    def _format_value(value):
        return str(value).upper()

    @classmethod
    def check(cls, value):
        if value is None:
            return value
        if type(value) is cls:
            return value
        try:
            return cls[cls._format_value(value)]
        except KeyError:
            return cls._missing_(value)


class Currency(_Enum):
    BTC = 'BTC'
    CLP = 'CLP'
    COP = 'COP'


class Market(_Enum):
    BTC_CLP = 'BTC-CLP'
    BTC_COP = 'BTC-COP'

    @staticmethod
    def _format_value(value):
        return str(value).replace('-', '_').upper()


class QuotationType(_Enum):
    BID_GIVEN_SIZE = 'bid_given_size'
    BID_GIVEN_EARNED_BASE = 'bid_given_earned_base'
    BID_GIVEN_SPENT_QUOTE = 'bid_given_spent_quote'
    ASK_GIVEN_SIZE = 'ask_given_size'
    ASK_GIVEN_EARNED_QUOTE = 'ask_given_earned_quote'
    ASK_GIVEN_SPENT_BASE = 'ask_given_spent_base'


class OrderType(_Enum):
    ASK = 'Ask'
    BID = 'Bid'


class OrderPriceType(_Enum):
    MARKET = 'market'
    LIMIT = 'limit'


class OrderState(_Enum):
    RECEIVED = 'received'
    PENDING = 'pending'
    TRADED = 'traded'
    CANCELING = 'canceling'
    CANCELED = 'canceled'


class BalanceEvent(_Enum):
    DEPOSIT_CONFIRM = 'deposit_confirm'
    WITHDRAWAL_CONFIRM = 'withdrawal_confirm'
    TRANSACTION = 'transaction'
    TRANSFER_CONFIRMATION = 'transfer_confirmation'


class ReportType(_Enum):
    CANDLESTICK = 'candlestick'
    AVERAGE_PRICES = 'average_prices'
