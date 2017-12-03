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
                "surbtc-w-%s" % wdraw.id,
                wdraw.created_at.isoformat(),
                "surbtc",
                wdraw.id,
                wdraw.state,
                currency,
                wdraw.amount.amount,
                wdraw.data.address,
                wdraw.data.tx_hash,
                wdraw.fee.amount
            )
            for wdraw in withdrawals
        ]

    def get_deposits(self, currency):
        deposits = self.client.deposits(
            currency=self.get_currency_mapping(currency)
        )
        return [
            (
                "surbtc-d-%s" % dep.id,
                dep.created_at.isoformat(),
                "surbtc",
                dep.id,
                dep.state,
                currency,
                dep.amount.amount,
                dep.data.address,
                dep.data.tx_hash, dep.fee.amount
            )
            for dep in deposits
        ]

    def get_orders(self, base, quote, state=None):
        market = self.get_pair_mapping(base, quote)
        orders = self.client.order_pages(market_id=market, page=1, per_page=300, state=state)
        for order in orders.orders:
            yield (
                "surbtc-o-%s-%s" % (order.account_id, order.id),
                order.created_at.isoformat(),
                "surbtc",
                order.account_id,
                order.id,
                base,
                quote,
                order.type,
                order.price_type,
                order.limit.currency if order.limit else None,
                order.limit.amount if order.limit else None,
                order.state,
                order.original_amount.currency,
                order.original_amount.amount,
                order.traded_amount.currency,
                order.traded_amount.amount,
                order.traded_amount.currency,
                order.traded_amount.amount,
                order.amount.currency,
                order.amount.amount,
                order.paid_fee.currency,
                order.paid_fee.amount,
                order.total_exchanged.currency,
                order.total_exchanged.amount
            )
