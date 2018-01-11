import pytz

from ..base import StandardClient
from .client_auth import SURBTCAuth

UTC_TIMEZONE = pytz.timezone('utc')

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
                wdraw.created_at.replace(tzinfo=UTC_TIMEZONE).isoformat(),
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
                dep.created_at.replace(tzinfo=UTC_TIMEZONE).isoformat(),
                "surbtc",
                dep.id,
                dep.state,
                currency,
                dep.amount.amount,
                dep.data.address,
                dep.data.tx_hash,
                dep.fee.amount
            )
            for dep in deposits
        ]

    def get_orders(self, base, quote, state=None):
        market = self.get_pair_mapping(base, quote)
        orders = self.client.order_pages(market_id=market, page=1, per_page=300, state=state)
        for order in orders.orders:
            yield (
                "surbtc-o-%s-%s" % (order.account_id, order.id),
                order.created_at.replace(tzinfo=UTC_TIMEZONE).isoformat(),
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
                order.amount.currency,
                order.amount.amount,
                order.paid_fee.currency,
                order.paid_fee.amount,
                order.total_exchanged.currency,
                order.total_exchanged.amount
            )

    def get_trades(self, base, quote, state=None):
        market = self.get_pair_mapping(base, quote)
        trades = self.client.trade_transaction_pages(market_id=market)
        for trade in trades.trade_transactions:
            yield (
                "surbtc-t-%s-%s" % (trade.market_id, trade.id),
                trade.id,
                trade.market_id,
                trade.created_at.replace(tzinfo=UTC_TIMEZONE).isoformat(),
                "surbtc",
                trade.ask_order.id,
                trade.ask_order.account_id,
                trade.ask_order.original_amount.amount,
                trade.ask_order.original_amount.currency,
                trade.ask_order.price_type,
                trade.bid_order.id,
                trade.bid_order.account_id,
                trade.bid_order.original_amount.amount,
                trade.bid_order.original_amount.currency,
                trade.bid_order.price_type,
                trade.triggering_order.id,
                trade.triggering_order.account_id,
                trade.triggering_order.total_exchanged.amount,
                trade.triggering_order.total_exchanged.currency,
                trade.triggering_order.traded_amount.amount,
                trade.triggering_order.traded_amount.currency,
                trade.triggering_order.type
            )
