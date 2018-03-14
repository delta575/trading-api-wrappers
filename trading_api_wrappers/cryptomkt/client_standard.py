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

    def markets(self):
        to_return_markets = {}
        for market in self.client.markets():
            base = market[0:3].lower()
            quote = market[3:].lower()
            market_name = self.get_pair_mapping(base, quote)
            to_return_markets[market_name] = {
                "name": market_name,
                "minimum_order_amount": 0.001,
                "base": base.lower(),
                "quote": quote.lower()
            }
        return to_return_markets


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

    def get_available_balance(self, currency):
        found_balance = self.client.balance().__getattribute__(currency.upper())
        if found_balance is None:
            return 0
        return float(found_balance.available)

    def get_ticker(self, base, quote, bid_ask='bid'):
        return self.client.ticker(self.get_pair_mapping(base, quote)).__getattribute__(bid_ask)

    def my_open_orders(self, base, quote):
        market = self.get_pair_mapping(base, quote)
        orders = self.client.active_orders(market)
        return [
            {
                'id': order.id,
                'type': 'ask' if order.type == 'sell' else 'bid',
                'market': order.market,
                'original_amount': order.amount.original,
                'remaining_amount': order.amount.remaining,
            } for order in orders.orders]

    def deploy_order(self, base, quote, order):
        market = self.get_pair_mapping(base, quote)
        if order["type"].lower() == 'ask':
            order_type = 'sell'
        elif order["type"].lower() == 'bid':
            order_type = 'buy'
        else:
            raise Exception("Incorrect order type")
        result = self.client.create_order(
            market,
            order_type,
            order["amount"],
            order["price"]
        )
        return result.id
