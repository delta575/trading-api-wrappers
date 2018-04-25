from ..base import Server

# API Server
PROTOCOL = 'https'
HOST = 'www.buda.com/api'
TEST_HOST = 'stg.buda.com/api'
VERSION = 'v2'


# Buda API server
class BudaServer(Server):

    def __init__(self, test, host=HOST):
        if test:
            host = TEST_HOST
        super().__init__(PROTOCOL, host, VERSION)
