from .. import market as _m
from .client_auth import OKXAuth
from .client_public import OKXPublic

__all__ = ["OKX"]


class OKX:
    """Global spot/derivatives venue."""

    models = _m
    Auth = OKXAuth
    Public = OKXPublic
