from . import constants as _c
from . import models as _m
from .client_auth import CryptoMKTAuth
from .client_public import CryptoMKTPublic


class CryptoMKT(object):
    # Models
    models = _m
    # Enum Types
    Currency = _c.Currency
    Market = _c.Market
    OrderType = _c.OrderType
    # Clients
    Auth = CryptoMKTAuth
    Public = CryptoMKTPublic


__all__ = [
    CryptoMKT,
]
