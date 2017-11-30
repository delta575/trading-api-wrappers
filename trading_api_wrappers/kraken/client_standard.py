from ..base import StandardClient
from .client_public import KrakenPublic

class KrakenStandard(StandardClient):
    client = KrakenPublic()

    @staticmethod
    def get_pair_mapping(base, quote):
        currency_mapping = {
            'btc': 'XXBT',
            'eth': 'XETH',
            'bch': 'BCH',
            'usd': 'ZUSD',
            'eur': 'ZEUR'
        }
        if base == 'bch':
            pair = currency_mapping[base]+currency_mapping[quote][1:]
        else:
            pair = currency_mapping[base]+currency_mapping[quote]
        return pair

    @classmethod
    def standarize_orderbook(cls, raw_orderbook):
        return cls.base_standarize_orderbook(
            raw_orderbook, lambda entry: (entry[1], entry[0])
        )

    def get_orderbook(self, base, quote):
        market = self.get_pair_mapping(base, quote)
        orderbook = self.client.order_book(market)['result'][market]
        return self.standarize_orderbook(orderbook)