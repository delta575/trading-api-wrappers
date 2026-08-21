from . import models as _m
from .clients import RipioAuth, RipioPublic

__all__ = [
    "Ripio",
]


class Ripio:
    models = _m
    Auth = RipioAuth
    Public = RipioPublic
