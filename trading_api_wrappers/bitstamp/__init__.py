from . import constants as _c
from .client_auth import BitstampAuth
from .client_public import BitstampPublic


class Bitstamp(object):
    # Enum Types
    CurrencyPair = _c.CurrencyPair
    TimeInterval = _c.TimeInterval
    # Clients
    Auth = BitstampAuth
    Public = BitstampPublic


__all__ = [
    'Bitstamp',
]
