from ..base import Currency, Market, _Enum


class Currency(Currency):
    ARS = dict(value="ARS")
    BRL = dict(value="BRL")
    BTC = dict(value="BTC")
    CLP = dict(value="CLP")
    ETH = dict(value="ETH", decimals=9)
    EUR = dict(value="EUR")
    USDT = dict(value="USDT")


class OrderType(_Enum):
    BUY = "buy"
    SELL = "sell"


class Market(Market):
    @staticmethod
    def _format_value(value):
        return str(value).replace("-", "").replace("_", "").upper()

    BTC_USDT = dict(value="BTCUSDT", base=Currency.BTC, quote=Currency.USDT)
    ETH_BTC = dict(value="ETHBTC", base=Currency.ETH, quote=Currency.BTC)
    ETH_USDT = dict(value="ETHUSDT", base=Currency.ETH, quote=Currency.USDT)
    BTC_CLP = dict(value="BTCCLP", base=Currency.BTC, quote=Currency.CLP)
    ETH_CLP = dict(value="ETHCLP", base=Currency.ETH, quote=Currency.CLP)
    BTC_ARS = dict(value="BTCARS", base=Currency.BTC, quote=Currency.ARS)
    BTC_BRL = dict(value="BTCBRL", base=Currency.BTC, quote=Currency.BRL)
