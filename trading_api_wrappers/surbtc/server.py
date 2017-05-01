from ..base import Server

# API Server
PROTOCOL = 'https'
HOST = 'www.surbtc.com/api'
TEST_HOST = 'stg.surbtc.com/api'
VERSION = 'v2'


# SURBTC API server
class SURBTCServer(Server):

    def __init__(self, test):
        host = HOST if not test else TEST_HOST
        Server.__init__(self, PROTOCOL, host, VERSION)
