from .. import market as _m
from .client_auth import BitsoAuth
from .client_public import BitsoPublic

__all__ = ["Bitso"]


class Bitso:
    """Mexican CEX. MXN order books via REST v3."""

    models = _m
    Auth = BitsoAuth
    Public = BitsoPublic
