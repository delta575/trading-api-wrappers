from datetime import datetime
from ..base import StandardClient
from .client_auth import KrakenAuth

class KrakenStandard(StandardClient):
    def __init__(self, key=False, secret=False, timeout=30):
        StandardClient.__init__(self)
        self.currency_mapping = {
            'btc': 'XXBT',
            'eth': 'XETH',
            'bch': 'BCH',
            'usd': 'ZUSD',
            'eur': 'ZEUR'
        }
        self.client = KrakenAuth(key=str(key), secret=str(secret), timeout=timeout)

    @staticmethod
    def get_pair_mapping(base, quote):
        if base == 'bch':
            pair = self.currency_mapping[base]+self.currency_mapping[quote][1:]
        else:
            pair = self.currency_mapping[base]+self.currency_mapping[quote]
        return pair

    def get_currency_mapping(self, currency):
        return self.currency_mapping[currency]

    @classmethod
    def standarize_orderbook(cls, raw_orderbook):
        return cls.base_standarize_orderbook(
            raw_orderbook, lambda entry: (entry[1], entry[0])
        )

    def get_orderbook(self, base, quote):
        market = self.get_pair_mapping(base, quote)
        orderbook = self.client.order_book(market)['result'][market]
        return self.standarize_orderbook(orderbook)

    def get_withdrawals(self, currency):
        kraken_currency = self.get_currency_mapping(currency)
        withdrawals = self.client.withdraw_status(
            kraken_currency, asset_class='currency'
        )['result']
        return [
            (
                "kraken-w-%s" % wdraw['refid'],
                datetime.fromtimestamp(wdraw['time']).isoformat(),
                "kraken",
                wdraw['refid'],
                wdraw['status'],
                currency,
                wdraw['amount'],
                wdraw.get('info'),
                wdraw.get('txid'),
                wdraw.get('fee', 0)
            )
            for wdraw in withdrawals
        ]

    def get_deposits(self, currency):
        kraken_currency = self.get_currency_mapping(currency)
        methods = self.client.deposit_methods(kraken_currency)['result']
        withdrawals = []
        for row_method in methods:
            method = row_method["method"]
            withdrawals += self.client.deposit_status(
                kraken_currency, method, asset_class='currency'
            )['result']
        return [
            (
                "kraken-w-%s" % wdraw['refid'],
                datetime.fromtimestamp(wdraw['time']).isoformat(),
                "kraken",
                wdraw['refid'],
                wdraw['status'],
                currency,
                wdraw['amount'],
                wdraw.get('info'),
                wdraw.get('txid'),
                wdraw.get('fee', 0)
            )
            for wdraw in withdrawals
        ]
