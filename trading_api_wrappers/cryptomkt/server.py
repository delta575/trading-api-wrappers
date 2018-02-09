from ..base import Server

# Server
PROTOCOL = 'https'
HOST = 'api.cryptomkt.com'
VERSION = 'v1'


# CryptoMKT server
class CryptoMKTServer(Server):
    def __init__(self):
        super().__init__(PROTOCOL, HOST, VERSION)
