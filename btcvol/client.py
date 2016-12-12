from common import Client

# API Server
PROTOCOL = 'https'
HOST = 'btcvol.info'

# API Paths
PATH_LATEST = 'latest'
PATH_ALL = 'all'


class BtcVol(object):
    
    def __init__(self, timeout=30):
        self.client = Client(PROTOCOL, HOST, version=None, timeout=timeout)

    def live(self):
        try:
            self.latest()
            return True
        except:
            return False

    def latest(self):
        url = self.client.url_for(PATH_LATEST)
        return self.client.get(url)

    def all(self):
        url = self.client.url_for(PATH_ALL)
        return self.client.get(url)
