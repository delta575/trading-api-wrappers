from . import constants as _c
from . import models as _m
from .client_public import CryptoMKTPublic


class CryptoMKT(CryptoMKTPublic):
    # Models
    models = _m
    # Enum Types
    Currency = _c.Currency
    Market = _c.Market
    OrderBook = _c.OrderBook
    TimeFrame = _c.TimeFrame
    # Clients
    Public = CryptoMKTPublic


__all__ = [
    CryptoMKT,
]
