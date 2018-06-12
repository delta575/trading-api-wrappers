# local
from ..base import Client, Server

# API Server
PROTOCOL = 'https'
HOST = 'bitcoinity.org'


class Bitcoinity(Client):
    def __init__(self, timeout: int=15, retry=None):
        super().__init__(Server(PROTOCOL, HOST), timeout, retry)

    def ticker(self,
               currency: str,
               exchange: str,
               span: str):
        return self.get('markets/get_ticker', params={
            'currency': currency,
            'exchange': exchange,
            'span': span,
        })
