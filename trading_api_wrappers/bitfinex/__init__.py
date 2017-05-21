from . import constants_v1 as _c1
from . import constants_v2 as _c2
from .client_auth_v1 import BitfinexAuth
from .client_public_v1 import BitfinexPublic
from .client_public_v2 import BitfinexPublic as BitfinexPublicV2


class Bitfinex(object):
    # Enum Types
    Currency = _c1.Currency
    Symbol = _c1.Symbol
    # Clients V1
    Auth = BitfinexAuth
    Public = BitfinexPublic


class BitfinexV2(object):
    # Enum Types
    # Currency = _c2.Currency
    BookPrecision = _c2.BookPrecision
    Symbol = _c2.Symbol
    # Clients
    # Auth = BitfinexAuth
    Public = BitfinexPublicV2


__all__ = [
    Bitfinex,
    BitfinexV2,
]
