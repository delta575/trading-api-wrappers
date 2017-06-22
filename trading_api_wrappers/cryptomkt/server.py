from ..base import Server

# Server
PROTOCOL = 'https'
HOST = 'www.cryptomkt.com/api'


# CryptoMKT server
class CryptoMKTServer(Server):
    def __init__(self):
        Server.__init__(self, PROTOCOL, HOST)
