from . import constants as _c
# from . import models as _m
from .client_auth import KrakenAuth
from .client_public import KrakenPublic


class Kraken(object):
    # Models
    # models = _m
    # Enum Types
    Currency = _c.Currency
    Symbols = _c.Symbol
    # Clients
    Auth = KrakenAuth
    Public = KrakenPublic


__all__ = [
    Kraken,
]
