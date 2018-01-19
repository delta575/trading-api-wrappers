from .client_auth import BitstampAuth
from .client_public import BitstampPublic
from .client_standard import BitstampStandard


class Bitstamp(object):
    # Clients
    Auth = BitstampAuth
    Public = BitstampPublic
    Standard = BitstampStandard


__all__ = [
    'Bitstamp',
]
