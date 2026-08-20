from .. import market as _m
from .client_auth import MercadoBitcoinAuth
from .client_public import MercadoBitcoinPublic

__all__ = ["MercadoBitcoin"]


class MercadoBitcoin:
    """Brazilian CEX. BRL books via Data API v4; trading via TAPI v3."""

    models = _m
    Auth = MercadoBitcoinAuth
    Public = MercadoBitcoinPublic
