# local
from ..base import Client, Server

# API Server
PROTOCOL = 'https'
HOST = 'btcvol.info'

# API Paths
PATH_LATEST = 'latest'
PATH_ALL = 'all'


class BtcVol(Client):

    def __init__(self, timeout=30):
        server = Server(PROTOCOL, HOST, version=None)
        Client.__init__(self, server, timeout)

    def latest(self):
        url = self.url_for(PATH_LATEST)
        return self.get(url)

    def all(self):
        url = self.url_for(PATH_ALL)
        return self.get(url)
