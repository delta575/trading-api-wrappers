from . import constants as _c
from . import models as _m
from .client_auth import CryptoMKTAuth
from .client_public import CryptoMKTPublic

__all__ = [
    "CryptoMKT",
]


class CryptoMKT:
    models = _m
    Currency = _c.Currency
    Market = _c.Market
    OrderType = _c.OrderType
    Auth = CryptoMKTAuth
    Public = CryptoMKTPublic
