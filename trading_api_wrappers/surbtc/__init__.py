from . import constants as _c
from . import models as _m
from .client_auth import SURBTCAuth
from .client_public import SURBTCPublic
from .client_standard import SURBTCStandard


class SURBTC(object):
    # Models
    models = _m
    # Enum Types
    BalanceEvent = _c.BalanceEvent
    Currency = _c.Currency
    Market = _c.Market
    OrderState = _c.OrderState
    OrderType = _c.OrderType
    OrderPriceType = _c.OrderPriceType
    QuotationType = _c.QuotationType
    ReportType = _c.ReportType
    # Clients
    Auth = SURBTCAuth
    Public = SURBTCPublic
    Standard = SURBTCStandard

class Buda(SURBTC):
    pass


__all__ = [
    SURBTC,
    Buda
]
