"""Compatibility alias. The live venue is NotBank, the CryptoMKT successor."""

from __future__ import annotations

import warnings

from .. import market as _m
from ..notbank import NotBank
from ..notbank.client_auth import NotBankAuth
from ..notbank.client_public import NotBankPublic

__all__ = ["CryptoMKT"]


def _warn():
    warnings.warn(
        "CryptoMKT is a compatibility alias of NotBank; use NotBank.",
        DeprecationWarning,
        stacklevel=3,
    )


class CryptoMKTPublic(NotBankPublic):
    def __init__(self, *args, **kwargs):
        _warn()
        super().__init__(*args, **kwargs)


class CryptoMKTAuth(NotBankAuth):
    def __init__(self, *args, **kwargs):
        _warn()
        super().__init__(*args, **kwargs)


class CryptoMKT(NotBank):
    """Deprecated alias of :class:`~trading_api_wrappers.notbank.NotBank`."""

    models = _m
    Auth = CryptoMKTAuth
    Public = CryptoMKTPublic
