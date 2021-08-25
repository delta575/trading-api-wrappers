from ..base import _Enum


class CurrencyPair(_Enum):
    BTC_USD = "btcusd"
    BTC_EUR = "btceur"
    EUR_USD = "eurusd"
    XRP_USD = "xrpusd"
    XRP_EUR = "xrpeur"
    XRP_BTC = "xrpbtc"
    LTC_USD = "ltcusd"
    LTC_EUR = "ltceur"
    LTC_BTC = "ltcbtc"
    ETH_USD = "ethusd"
    ETH_EUR = "etheur"
    ETH_BTC = "ethbtc"
    BCH_USD = "bchusd"
    BCH_EUR = "bcheur"
    BCH_BTC = "bchbtc"


class TimeInterval(_Enum):
    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"
