import pytz
from datetime import datetime
from hashlib import md5

from ..base import StandardClient
from .client_auth import BudaAuth

UTC_TIMEZONE = pytz.timezone('utc')

class BudaStandard(StandardClient):
    def __init__(self, key=False, secret=False, timeout=30):
        StandardClient.__init__(self)
        self.client = BudaAuth(key=str(key), secret=str(secret), timeout=timeout)

    @staticmethod
    def name():
        return "Buda"

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

    def markets(self):
        to_return_markets = {}
        for market in self.client.markets():
            to_return_markets[market.name] = {
                "name": market.name,
                "minimum_order_amount": market.minimum_order_amount.amount,
                "base": market.base_currency.lower(),
                "quote": market.quote_currency.lower()
            }
        return to_return_markets

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
                wdraw.created_at.replace(tzinfo=UTC_TIMEZONE).isoformat().split(".")[0],
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
                dep.created_at.replace(tzinfo=UTC_TIMEZONE).isoformat().split(".")[0],
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
                order.created_at.replace(tzinfo=UTC_TIMEZONE).isoformat().split(".")[0],
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

    def get_trades(self, base, quote, timestamp=None):
        market_id = self.get_pair_mapping(base, quote)
        params = {}
        if timestamp is not None:
            params['timestamp'] = timestamp
        url = self.client.url_for('markets/%s/trades', market_id)
        data = self.client.get(url, params=params)

        for trade in data['trades']['entries']:
            timestamp_ = (1.0*int(trade[0]))/1000
            date_iso = datetime.utcfromtimestamp(timestamp_).isoformat()
            trade_id = md5((",".join([str(x) for x in trade])).encode('utf-8')).hexdigest()[:9]
            yield (
                "surbtc-t-%s-%s" % (market_id, trade_id),
                trade_id,
                market_id,
                date_iso,
                "surbtc",
                base,
                float(trade[1]),
                quote,
                float(trade[2]),
                trade[3]
            )

    def get_balance(self, currency):
        return float(self.client.balance(currency).amount.amount)

    def get_available_balance(self, currency):
        return float(self.client.balance(currency).available_amount.amount)

    def get_ticker(self, base, quote, bid_ask='bid'):
        # TODO: refactor this
        if bid_ask == 'bid':
            return float(
                self.client.ticker(self.get_pair_mapping(base, quote)).max_bid.amount
            )
        elif bid_ask == 'ask':
            return float(
                self.client.ticker(self.get_pair_mapping(base, quote)).max_ask.amount
            )

    def my_open_orders(self, base, quote):
        market = self.get_pair_mapping(base, quote)
        orders = self.client.order_pages(
            market, state='pending', per_page=300
        ).orders
        return [
            {
                'id': order.id,
                'type': order.type.lower(),
                'market': order.market_id,
                'original_amount': order.original_amount.amount,
                'remaining_amount': order.original_amount.amount - order.traded_amount.amount
            } for order in orders
        ]

    def deploy_order(self, base, quote, order):
        market = self.get_pair_mapping(base, quote)
        prepared_order = {
            "order": {
                "limit": order["price"],
                "amount": order["amount"],
                "type": order["type"],
                "price_type": order["price_type"]
            }
        }
        result = self.client.new_order_payload(market, prepared_order)
        return result.id
