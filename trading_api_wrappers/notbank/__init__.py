from .. import market as _m
from .client_auth import NotBankAuth
from .client_public import NotBankPublic

__all__ = ["NotBank"]


class NotBank:
    """Chilean CEX successor of CryptoMKT. AlphaPoint /AP REST."""

    models = _m
    Auth = NotBankAuth
    Public = NotBankPublic
