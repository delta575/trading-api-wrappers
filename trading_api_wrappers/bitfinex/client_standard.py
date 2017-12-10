from datetime import datetime
from ..base import StandardClient
from .client_auth_v1 import BitfinexAuth

class BitfinexStandard(StandardClient):
    def __init__(self, key=False, secret=False, timeout=30):
        StandardClient.__init__(self)
        self.client = BitfinexAuth(key=str(key), secret=str(secret), timeout=timeout)

    @classmethod
    def get_pair_mapping(cls, base, quote):
        return cls.get_currency_mapping(base) + cls.get_currency_mapping(quote)

    @staticmethod
    def get_currency_mapping(currency):
        return currency.lower()

    @classmethod
    def standarize_orderbook(cls, raw_orderbook):
        return cls.base_standarize_orderbook(
            raw_orderbook, lambda entry: (entry['amount'], entry['price'])
        )

    def get_orderbook(self, base, quote):
        market = self.get_pair_mapping(base, quote)
        orderbook = self.client.order_book(market)
        return self.standarize_orderbook(orderbook)

    def format_movements(self, row):
        return (
            "bitfinex-w-%s" % row['id'],
            datetime.fromtimestamp(row['timestamp_created']).isoformat(),
            "bitfinex",
            row['id'],
            row['status'],
            currency,
            row['amount'],
            row.get('address', ''),
            row.get('txid', ''),
            row.get('fee', 0),
        )
    def get_withdrawals(self, currency):
        withdrawals = self.client.movements(
            currency=self.get_currency_mapping(currency)
        )
        return [
            self.format_movements(wdraw)
            for wdraw in withdrawals
            if wdraw['type'] == 'WITHDRAWAL'
        ]

    def get_deposits(self, currency):
        deposits = self.client.deposits(
            currency=self.get_currency_mapping(currency)
        )
        return [
            self.format_movements(wdraw)
            for wdraw in withdrawals
            if wdraw['type'] == 'DEPOSIT'
        ]
