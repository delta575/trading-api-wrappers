from trading_api_wrappers.base import Server

PROTOCOL = 'https'
HOST = 'api.bitfinex.com'
VERSION = 'v1'


# Bitfinex API server
class BitfinexServer(Server):
    def __init__(self):
        Server.__init__(self, PROTOCOL, HOST, VERSION)


# Bitfinex supported symbols
class Symbols:
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


# Bitfinex supported currencies
class Currencies:
    USD = 'usd'
    BTC = 'btc'
