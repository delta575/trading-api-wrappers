from ..base import Server

# Server
PROTOCOL = 'https'
HOST = 'api.cryptomkt.com'
VERSION = 'v1'


# CryptoMKT server
class CryptoMKTServer(Server):
    def __init__(self):
        Server.__init__(self, PROTOCOL, HOST, VERSION)
