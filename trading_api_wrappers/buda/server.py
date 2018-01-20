from ..base import Server

# API Server
PROTOCOL = 'https'
HOST = 'www.buda.com/api'
TEST_HOST = 'stg.buda.com/api'
VERSION = 'v2'


# Buda API server
class BudaServer(Server):

    def __init__(self, test):
        host = HOST if not test else TEST_HOST
        super(BudaServer, self).__init__(PROTOCOL, host, VERSION)
