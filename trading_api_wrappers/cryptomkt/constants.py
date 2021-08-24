from ..base import _Enum, Market, Currency

# Limits
ORDERS_LIMIT = 100


class Currency(Currency):
    ARS = dict(value="ARS")
    BRL = dict(value="BRL")
    BTC = dict(value="BTC")
    CLP = dict(value="CLP")
    EOS = dict(value="EOS")
    ETH = dict(value="ETH", decimals=9)
    EUR = dict(value="EUR")
    MXN = dict(value="MXN")
    XLM = dict(value="XLM")


class OrderType(_Enum):
    BUY = "buy"
    SELL = "sell"


class Market(Market):
    BTC_ARS = dict(value="BTCARS", base=Currency.BTC, quote=Currency.ARS)
    BTC_BRL = dict(value="BTCBRL", base=Currency.BTC, quote=Currency.BRL)
    BTC_CLP = dict(value="BTCCLP", base=Currency.BTC, quote=Currency.CLP)
    BTC_EUR = dict(value="BTCEUR", base=Currency.BTC, quote=Currency.EUR)
    BTC_MXN = dict(value="BTCMXN", base=Currency.BTC, quote=Currency.MXN)
    EOS_ARS = dict(value="EOSARS", base=Currency.EOS, quote=Currency.ARS)
    EOS_BRL = dict(value="EOSBRL", base=Currency.EOS, quote=Currency.BRL)
    EOS_CLP = dict(value="EOSCLP", base=Currency.EOS, quote=Currency.CLP)
    EOS_EUR = dict(value="EOSEUR", base=Currency.EOS, quote=Currency.EUR)
    EOS_MXN = dict(value="EOSMXN", base=Currency.EOS, quote=Currency.MXN)
    ETH_ARS = dict(value="ETHARS", base=Currency.ETH, quote=Currency.ARS)
    ETH_BRL = dict(value="ETHBRL", base=Currency.ETH, quote=Currency.BRL)
    ETH_CLP = dict(value="ETHCLP", base=Currency.ETH, quote=Currency.CLP)
    ETH_EUR = dict(value="ETHEUR", base=Currency.ETH, quote=Currency.EUR)
    ETH_MXN = dict(value="ETHMXN", base=Currency.ETH, quote=Currency.MXN)
    XLM_ARS = dict(value="XLMARS", base=Currency.XLM, quote=Currency.ARS)
    XLM_BRL = dict(value="XLMBRL", base=Currency.XLM, quote=Currency.BRL)
    XLM_CLP = dict(value="XLMCLP", base=Currency.XLM, quote=Currency.CLP)
    XLM_EUR = dict(value="XLMEUR", base=Currency.XLM, quote=Currency.EUR)
    XLM_MXN = dict(value="XLMMXN", base=Currency.XLM, quote=Currency.MXN)


class TimeFrame(_Enum):
    DAYS_1 = 1440
    HOURS_1 = 60
    MINUTES_15 = 15
    MINUTES_5 = 5
    MINUTES_1 = 1

    @staticmethod
    def _format_value(value):
        values = {
            1440: "DAYS_1",
            60: "HOURS_1",
            15: "MINUTES_15",
            5: "MINUTES_5",
            1: "MINUTES_1",
        }
        return values[value]
