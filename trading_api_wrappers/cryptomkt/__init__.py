from . import constants as _c
from . import models as _m
from .client_public import CryptoMKTPublic
from .client_standard import CryptoMKTStandard


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
    Standard = CryptoMKTStandard


__all__ = [
    CryptoMKT,
]
