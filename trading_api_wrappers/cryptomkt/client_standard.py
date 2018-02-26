from ..base import StandardClient
from .client_public import CryptoMKTPublic
from .client_auth import CryptoMKTAuth

class CryptoMKTStandard(StandardClient):
    def __init__(self, key=False, secret=False, timeout=30):
        StandardClient.__init__(self)
        self.client = CryptoMKTAuth(key=str(key), secret=str(secret), timeout=timeout)

    @staticmethod
    def name():
        return "CryptoMKT"

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

    def get_balance(self, currency):
        found_balance = self.client.balance().__getattribute__(currency.upper())
        if found_balance is None:
            return 0
        return float(found_balance.balance)

    def get_ticker(self, base, quote, bid_ask='bid'):
        return self.client.ticker(self.get_pair_mapping(base, quote)).__getattribute__(bid_ask)
