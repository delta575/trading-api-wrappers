from ..base import _Enum


# API paths
class Path(object):
    # Public
    TICKER = 'pubticker/%s'
    STATS = 'stats/%s'
    TODAY = 'today/%s'
    LEND_BOOK = 'lendbook/%s'
    ORDER_BOOK = 'book/%s'
    TRADES = 'trades/%s'
    LENDS = 'lends/%s'
    SYMBOLS = 'symbols'
    SYMBOLS_DETAILS = 'symbols_details'
    # Info
    ACCOUNT_INFO = 'account_infos'
    SUMMARY = 'summary'
    KEY_INFO = 'key_info'
    MARGIN_INFO = 'margin_infos'
    BALANCES = 'balances'
    # Movements
    DEPOSIT_NEW = 'deposit/new'
    TRANSFER = 'transfer'
    WITHDRAW = 'withdraw'
    # Orders
    ORDER_NEW = 'order/new'
    ORDER_CANCEL = 'order/cancel'
    ORDER_CANCEL_ALL = 'order/cancel/all'
    ORDER_STATUS = 'order/status'
    ORDERS = 'orders'
    # Positions
    POSITIONS = 'positions'
    POSITION_CLAIM = 'position/claim'
    # Historical Data
    HISTORY = 'history'
    HISTORY_MOVEMENTS = 'history/movements'
    PAST_TRADES = 'mytrades'
    # Margin Funding
    OFFER_NEW = 'offer/new'
    OFFER_CANCEL = 'offer/cancel'
    OFFER_STATUS = 'offer/status'
    OFFERS = 'offers'


# Bitfinex supported symbols
class Symbol(_Enum):
    BTCUSD = 'btcusd'
    LTCUSD = 'ltcusd'
    ETHUSD = 'ethusd'
    ETHBTC = 'ethbtc'
    ETCUSD = 'etcusd'
    ETCBTC = 'etcbtc'
    BFXUSD = 'bfxusd'
    BFXBTC = 'bfxbtc'
    RRTUSD = 'rrtusd'
    RRTBTC = 'rrtbtc'
    ZECUSD = 'zecusd'
    ZECBTC = 'zecbtc'
    XMRUSD = 'xmrusd'
    XMRBTC = 'xmrbtc'
    BCHUSD = 'bchusd'
    BCHBTC = 'bchbtc'
    BCHETH = 'bcheth'


# Bitfinex supported currencies
class Currency(_Enum):
    USD = 'usd'
    BTC = 'btc'
    ETH = 'eth'
    BCH = 'bch'


# Bitfinex supported symbols
class SymbolV2(_Enum):
    BTCUSD = 'tBTCUSD'
    BCHUSD = 'tBCHUSD'
    BCHBTC = 'tBCHBTC'
    LTCUSD = 'tLTCUSD'
    ETHUSD = 'tETHUSD'
    ETHBTC = 'tETHBTC'
    ETCUSD = 'tETCUSD'
    ETCBTC = 'tETCBTC'
    BFXUSD = 'tBFXUSD'
    BFXBTC = 'tBFXBTC'
    RRTUSD = 'tRRTUSD'
    RRTBTC = 'tRRTBTC'
    ZECUSD = 'tZECUSD'
    ZECBTC = 'tZECBTC'
    XMRUSD = 'tXMRUSD'
    XMRBTC = 'tXMRBTC'
