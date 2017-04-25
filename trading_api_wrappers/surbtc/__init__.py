from . import constants as _c
from . import models as _m
from .client_auth import SURBTCAuth
from .client_public import SURBTCPublic


class SURBTC(object):
    # Models
    models = _m
    # Enum Types
    Currency = _c.Currency
    Market = _c.Market
    OrderType = _c.OrderType
    OrderState = _c.OrderState
    OrderPriceType = _c.OrderPriceType
    BalanceEvent = _c.BalanceEvent
    QuotationType = _c.QuotationType
    ReportType = _c.ReportType
    # Clients
    Auth = SURBTCAuth
    Public = SURBTCPublic


__all__ = [
    SURBTCAuth,
    SURBTCPublic,
]
