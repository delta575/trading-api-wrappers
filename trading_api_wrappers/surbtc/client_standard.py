from ..base import StandardClient
from .client_auth import SURBTCAuth

class SURBTCStandard(StandardClient):
    def __init__(self, key=False, secret=False, timeout=30):
        StandardClient.__init__(self)
        self.client = SURBTCAuth(key=str(key), secret=str(secret), timeout=timeout)

    @staticmethod
    def get_pair_mapping(base, quote):
        return base + '-' + quote

    @staticmethod
    def get_currency_mapping(currency):
        return currency.upper()

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

    def get_withdrawals(self, currency):
        withdrawals = self.client.withdrawals(
            currency=self.get_currency_mapping(currency)
        )
        return [
            (
                wdraw.id, wdraw.created_at.isoformat(), wdraw.state,
                currency, wdraw.amount.amount, wdraw.data.address,
                wdraw.data.tx_hash, wdraw.fee.amount
            )
            for wdraw in withdrawals
        ]

    def get_deposits(self, currency):
        deposits = self.client.deposits(
            currency=self.get_currency_mapping(currency)
        )
        return [
            (
                dep.id, dep.created_at.isoformat(), dep.state,
                currency, dep.amount.amount, dep.data.address,
                dep.data.tx_hash, dep.fee.amount
            )
            for dep in deposits
        ]