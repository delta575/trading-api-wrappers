from . import constants as _c
from . import models as _m
from .client import CryptoMKTPublic


class CryptoMKT(CryptoMKTPublic):
    # Models
    models = _m
    # Enum Types
    Currency = _c.Currency
    Market = _c.Market
    TimeFrame = _c.TimeFrame


__all__ = [
    CryptoMKT,
]
