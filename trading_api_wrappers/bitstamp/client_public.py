# local
from ..base import Client
from .server import BitstampServer


class BitstampPublic(Client):

    error_key = 'error'

    def __init__(self, timeout=30):
        Client.__init__(self, BitstampServer(), timeout)
