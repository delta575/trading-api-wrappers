from . import constants as _c
from .client_auth import BitfinexAuth
from .client_public import BitfinexPublic


class Bitfinex(object):
    # Enum Types
    Currency = _c.Currency
    Symbol = _c.Symbol
    # Clients
    Auth = BitfinexAuth
    Public = BitfinexPublic


__all__ = [
    Bitfinex,
]
