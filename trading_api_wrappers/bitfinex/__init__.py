from . import constants_v1 as _c1
from . import constants_v2 as _c2
from . import models_v2 as _m2
from .client_auth_v1 import BitfinexAuth
from .client_public_v1 import BitfinexPublic
from .client_public_v2 import BitfinexPublic as BitfinexPublicV2

__all__ = [
    "Bitfinex",
    "BitfinexV2",
]


class Bitfinex:
    # Enum Types
    Currency = _c1.Currency
    Symbol = _c1.Symbol
    # Clients V1
    Auth = BitfinexAuth
    Public = BitfinexPublic


class BitfinexV2:
    # Models
    models = _m2
    # Enum Types
    BookPrecision = _c2.BookPrecision
    Symbol = _c2.Symbol
    # Clients
    # TODO: Implement Bitfinex v2 Auth client
    # Auth = BitfinexAuthV2
    Public = BitfinexPublicV2
