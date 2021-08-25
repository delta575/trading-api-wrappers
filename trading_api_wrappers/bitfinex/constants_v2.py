from ..base import _Enum


# Bitfinex supported symbols
class Symbol(_Enum):
    BCHUSD = "tBCHUSD"
    BCHBTC = "tBCHBTC"
    BTCUSD = "tBTCUSD"
    LTCUSD = "tLTCUSD"
    ETHUSD = "tETHUSD"
    ETHBTC = "tETHBTC"
    ETCUSD = "tETCUSD"
    ETCBTC = "tETCBTC"
    BFXUSD = "tBFXUSD"
    BFXBTC = "tBFXBTC"
    RRTUSD = "tRRTUSD"
    RRTBTC = "tRRTBTC"
    ZECUSD = "tZECUSD"
    ZECBTC = "tZECBTC"
    XMRUSD = "tXMRUSD"
    XMRBTC = "tXMRBTC"


# Bitfinex supported currencies
class Currency(_Enum):
    BCH = "bch"
    BTC = "btc"
    ETH = "eth"
    USD = "usd"


# Bitfinex supported precisions
class BookPrecision(_Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    R0 = "R0"
