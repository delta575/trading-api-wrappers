from ..base import _Enum


# Bitfinex supported symbols
class Symbol(_Enum):
    BTCUSD = "btcusd"
    LTCUSD = "ltcusd"
    ETHUSD = "ethusd"
    ETHBTC = "ethbtc"
    ETCUSD = "etcusd"
    ETCBTC = "etcbtc"
    BFXUSD = "bfxusd"
    BFXBTC = "bfxbtc"
    RRTUSD = "rrtusd"
    RRTBTC = "rrtbtc"
    ZECUSD = "zecusd"
    ZECBTC = "zecbtc"
    XMRUSD = "xmrusd"
    XMRBTC = "xmrbtc"
    BCHUSD = "bchusd"
    BCHBTC = "bchbtc"
    BCHETH = "bcheth"


# Bitfinex supported currencies
class Currency(_Enum):
    USD = "usd"
    BTC = "btc"
    ETH = "eth"
    BCH = "bch"
    BFX = "bfx"
