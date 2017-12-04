from ..base import _Enum, _Market, _Currency

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
    WITHDRAWALS = 'currencies/%s/withdrawals'
    DEPOSITS = 'currencies/%s/deposits'


class Currency(_Currency):
    BCH = dict(value='BCH', decimals=8)
    BTC = dict(value='BTC', decimals=8)
    CLP = dict(value='CLP')
    COP = dict(value='COP')
    ETH = dict(value='ETH', decimals=18)
    PEN = dict(value='PEN')


class Market(_Market):
    BCH_BTC = dict(value='BCH-BTC', base=Currency.BCH, quote=Currency.BTC)
    BCH_CLP = dict(value='BCH-CLP', base=Currency.BCH, quote=Currency.CLP)
    BCH_COP = dict(value='BCH-COP', base=Currency.BCH, quote=Currency.COP)
    BCH_PEN = dict(value='BCH-PEN', base=Currency.BCH, quote=Currency.PEN)
    BTC_CLP = dict(value='BTC-CLP', base=Currency.BTC, quote=Currency.CLP)
    BTC_COP = dict(value='BTC-COP', base=Currency.BTC, quote=Currency.COP)
    BTC_PEN = dict(value='BTC-PEN', base=Currency.BTC, quote=Currency.PEN)
    ETH_BTC = dict(value='ETH-BTC', base=Currency.ETH, quote=Currency.BTC)
    ETH_CLP = dict(value='ETH-CLP', base=Currency.ETH, quote=Currency.CLP)
    ETH_COP = dict(value='ETH-COP', base=Currency.ETH, quote=Currency.COP)
    ETH_PEN = dict(value='ETH-PEN', base=Currency.ETH, quote=Currency.PEN)


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
