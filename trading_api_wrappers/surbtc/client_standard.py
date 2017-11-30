from ..base import StandardClient
from .client_public import SURBTCPublic

class SURBTCStandard(StandardClient):
    client = SURBTCPublic()

    @staticmethod
    def get_pair_mapping(base, quote):
        return base + '-' + quote

    @classmethod
    def standarize_orderbook(cls, raw_orderbook):
        return cls.base_standarize_orderbook(
            raw_orderbook, lambda entry: (entry.amount, entry.price)
        )

    def get_orderbook(self, base, quote):
        market = self.get_pair_mapping(base, quote)
        tmp_orderbook = self.client.order_book(market)
        orderbook = {}
        orderbook['bids'] = tmp_orderbook.bids
        orderbook['asks'] = tmp_orderbook.asks
        return self.standarize_orderbook(orderbook)
