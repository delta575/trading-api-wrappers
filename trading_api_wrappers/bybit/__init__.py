from .. import market as _m
from .client_auth import BybitAuth
from .client_public import BybitPublic

__all__ = ["Bybit"]


class Bybit:
    """Global spot/derivatives venue."""

    models = _m
    Auth = BybitAuth
    Public = BybitPublic
