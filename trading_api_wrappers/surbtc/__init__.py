from . import constants as _c
from . import models as _m
from .client_auth import SURBTCAuth
from .client_public import SURBTCPublic


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


__all__ = [
    SURBTC,
]
