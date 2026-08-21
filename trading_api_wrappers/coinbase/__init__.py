from .. import market as _m
from .client_auth import CoinbaseAuth
from .client_public import CoinbasePublic

__all__ = ["Coinbase"]


class Coinbase:
    """Coinbase Exchange USD book (not Advanced Trade retail)."""

    models = _m
    Auth = CoinbaseAuth
    Public = CoinbasePublic
