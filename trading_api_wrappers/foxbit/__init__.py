from .. import market as _m
from .client_auth import FoxbitAuth
from .client_public import FoxbitPublic

__all__ = ["Foxbit"]


class Foxbit:
    """Brazilian CEX. BRL books and Pix rails via REST v3."""

    models = _m
    Auth = FoxbitAuth
    Public = FoxbitPublic
