from __future__ import annotations

import functools
import socket
import unittest

from decouple import config

from trading_api_wrappers.errors import InvalidResponse

_PLACEHOLDER = "XXXXXXXX"


def env(name: str, default: str | None = None) -> str | None:
    """Return an env var, treating missing values and placeholders as unset."""
    value = config(name, default=default)
    if value in (None, "", _PLACEHOLDER):
        return None
    return str(value)


def skip_without(*names: str):
    """Skip a test class or method when required credentials are missing."""
    missing = [name for name in names if not env(name)]
    reason = f"missing credentials: {', '.join(missing)}"
    return unittest.skipIf(bool(missing), reason)


def skip_unless_host(host: str, port: int = 443):
    """Skip when a remote API host cannot be resolved."""
    try:
        socket.getaddrinfo(host, port)
        reachable = True
    except OSError:
        reachable = False
    return unittest.skipUnless(reachable, f"{host} is not reachable")


def skip_http(*codes: int):
    """Skip a test when the venue answers with one of the given HTTP codes.

    Used for geo-blocks (Binance 451, Bybit 403) and Orionx's unsigned 500.
    """
    if not codes:
        codes = (403, 451)

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            try:
                return fn(self, *args, **kwargs)
            except InvalidResponse as exc:
                status = getattr(exc.response, "status_code", None)
                if status in codes:
                    raise unittest.SkipTest(
                        f"HTTP {status} from {getattr(exc.response, 'url', '')}"
                    ) from exc
                raise

        return wrapper

    return decorator
