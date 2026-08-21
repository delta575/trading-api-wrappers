from .. import market as _m
from .client_auth import BinanceAuth
from .client_public import BinancePublic

__all__ = ["Binance"]


class Binance:
    """Global spot venue (~35–45% of spot volume)."""

    models = _m
    Auth = BinanceAuth
    Public = BinancePublic
