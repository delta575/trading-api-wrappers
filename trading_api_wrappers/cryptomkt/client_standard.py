from ..base import StandardClient
from .client_public import CryptoMKTPublic

class CryptoMKTStandard(StandardClient):
    client = CryptoMKTPublic()

    @staticmethod
    def get_pair_mapping(base, quote):
        return base + quote

    @classmethod
    def standarize_orderbook(cls, raw_orderbook):
        return cls.base_standarize_orderbook(
            raw_orderbook, lambda entry: (entry.amount, entry.price)
        )

    def get_orderbook(self, base, quote):
        market = self.get_pair_mapping(base, quote)
        orderbook = {}
        orderbook['bids'] = self.client.order_book(market, 'buy')[0]
        orderbook['asks'] = self.client.order_book(market, 'sell')[0]
        return self.standarize_orderbook(orderbook)
