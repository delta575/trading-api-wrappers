from .. import market as _m
from .client_auth import OrionxAuth
from .client_public import OrionxPublic

__all__ = ["Orionx"]


class Orionx:
    """Chilean CEX (CLP). GraphQL API at api2.orionx.com."""

    models = _m
    Auth = OrionxAuth
    Public = OrionxPublic
