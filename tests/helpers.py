from __future__ import annotations

import unittest

from decouple import config

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
