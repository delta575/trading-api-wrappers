from ..base import StandardClient
from .client_public_v1 import BitfinexPublic

class BitfinexStandard(StandardClient):
    client = BitfinexPublic()

    @staticmethod
    def get_pair_mapping(base, quote):
        return base + quote

    @classmethod
    def standarize_orderbook(cls, raw_orderbook):
        return cls.base_standarize_orderbook(
            raw_orderbook, lambda entry: (entry['amount'], entry['price'])
        )

    def get_orderbook(self, base, quote):
        market = self.get_pair_mapping(base, quote)
        orderbook = self.client.order_book(market)
        return self.standarize_orderbook(orderbook)