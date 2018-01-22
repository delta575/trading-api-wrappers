# local
from ..base import Client
from .server import BitstampServer


class BitstampPublic(Client):

    error_key = 'error'

    def __init__(self, timeout=30):
        Client.__init__(self, BitstampServer(), timeout)

    def ticker(self, symbol):
        url = self.url_for('v2/ticker/%s/' % symbol)
        return self.get(url)
