from ..base import Server

# API Server
PROTOCOL = 'https'
HOST = 'www.buda.com/api'
TEST_HOST = 'stg.surbtc.com/api'  # TODO: change to buda.com
VERSION = 'v2'


# Buda API server
class BudaServer(Server):

    def __init__(self, test, host=None):
        host = host or HOST
        if test:
            host = TEST_HOST
        super().__init__(PROTOCOL, host, VERSION)
