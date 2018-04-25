from ..base import Server

# API Server
PROTOCOL = 'https'
HOST = 'www.buda.com/api'
VERSION = 'v2'


# Buda API server
class BudaServer(Server):

    def __init__(self, host):
        host = host or HOST
        super().__init__(PROTOCOL, host, VERSION)
