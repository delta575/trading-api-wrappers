from . import constants as _c
from .client_auth import BitstampAuth
from .client_public import BitstampPublic

__all__ = [
    'Bitstamp',
]


class Bitstamp(object):
    # Enum Types
    CurrencyPair = _c.CurrencyPair
    TimeInterval = _c.TimeInterval
    # Clients
    Auth = BitstampAuth
    Public = BitstampPublic
