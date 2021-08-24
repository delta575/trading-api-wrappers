from ..base import _Enum, Currency, Market

# Limits
ORDERS_LIMIT = 300
TRANSFERS_LIMIT = 300


class Currency(Currency):
    ARS = dict(value="ARS")
    BCH = dict(value="BCH", decimals=8)
    BTC = dict(value="BTC", decimals=8)
    CLP = dict(value="CLP")
    COP = dict(value="COP")
    ETH = dict(value="ETH", decimals=9)
    LTC = dict(value="LTC", decimals=8)
    PEN = dict(value="PEN")
    USDC = dict(value="USDC")


class Market(Market):
    BCH_ARS = dict(value="BCH-ARS", base=Currency.BCH, quote=Currency.ARS)
    BCH_BTC = dict(value="BCH-BTC", base=Currency.BCH, quote=Currency.BTC)
    BCH_CLP = dict(value="BCH-CLP", base=Currency.BCH, quote=Currency.CLP)
    BCH_COP = dict(value="BCH-COP", base=Currency.BCH, quote=Currency.COP)
    BTC_ARS = dict(value="BTC-ARS", base=Currency.BTC, quote=Currency.ARS)
    BCH_PEN = dict(value="BCH-PEN", base=Currency.BCH, quote=Currency.PEN)
    BTC_CLP = dict(value="BTC-CLP", base=Currency.BTC, quote=Currency.CLP)
    BTC_COP = dict(value="BTC-COP", base=Currency.BTC, quote=Currency.COP)
    BTC_PEN = dict(value="BTC-PEN", base=Currency.BTC, quote=Currency.PEN)
    ETH_ARS = dict(value="ETH-ARS", base=Currency.ETH, quote=Currency.ARS)
    ETH_BTC = dict(value="ETH-BTC", base=Currency.ETH, quote=Currency.BTC)
    ETH_CLP = dict(value="ETH-CLP", base=Currency.ETH, quote=Currency.CLP)
    ETH_COP = dict(value="ETH-COP", base=Currency.ETH, quote=Currency.COP)
    ETH_PEN = dict(value="ETH-PEN", base=Currency.ETH, quote=Currency.PEN)
    LTC_ARS = dict(value="LTC-ARS", base=Currency.LTC, quote=Currency.ARS)
    LTC_BTC = dict(value="LTC-BTC", base=Currency.LTC, quote=Currency.BTC)
    LTC_CLP = dict(value="LTC-CLP", base=Currency.LTC, quote=Currency.CLP)
    LTC_COP = dict(value="LTC-COP", base=Currency.LTC, quote=Currency.COP)
    LTC_PEN = dict(value="LTC-PEN", base=Currency.LTC, quote=Currency.PEN)
    BTC_USDC = dict(value="BTC-USDC", base=Currency.BTC, quote=Currency.USDC)
    USDC_ARS = dict(value="USDC-ARS", base=Currency.USDC, quote=Currency.ARS)
    USDC_CLP = dict(value="USDC-CLP", base=Currency.USDC, quote=Currency.CLP)
    USDC_COP = dict(value="USDC-COP", base=Currency.USDC, quote=Currency.COP)
    USDC_PEN = dict(value="USDC-PEN", base=Currency.USDC, quote=Currency.PEN)


class QuotationType(_Enum):
    BID_GIVEN_SIZE = "bid_given_size"
    BID_GIVEN_EARNED_BASE = "bid_given_earned_base"
    BID_GIVEN_SPENT_QUOTE = "bid_given_spent_quote"
    ASK_GIVEN_SIZE = "ask_given_size"
    ASK_GIVEN_EARNED_QUOTE = "ask_given_earned_quote"
    ASK_GIVEN_SPENT_BASE = "ask_given_spent_base"


class OrderType(_Enum):
    ASK = "Ask"
    BID = "Bid"


class OrderPriceType(_Enum):
    MARKET = "market"
    LIMIT = "limit"


class OrderState(_Enum):
    RECEIVED = "received"
    PENDING = "pending"
    TRADED = "traded"
    CANCELING = "canceling"
    CANCELED = "canceled"


class BalanceEvent(_Enum):
    DEPOSIT_CONFIRM = "deposit_confirm"
    WITHDRAWAL_CONFIRM = "withdrawal_confirm"
    TRANSACTION = "transaction"
    TRANSFER_CONFIRMATION = "transfer_confirmation"


class ReportType(_Enum):
    CANDLESTICK = "candlestick"
    AVERAGE_PRICES = "average_prices"
