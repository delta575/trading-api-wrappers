from collections import namedtuple
from datetime import datetime


def parse_datetime(datetime_str):
    if datetime_str:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')


def parse_iso_datetime(datetime_str):
    if datetime_str:
        return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f')


def check_null(value):
    return value if value != 'null' else None


def int_or_null(value):
    value = check_null(value)
    return int(value) if value else None


def float_or_null(value):
    value = check_null(value)
    return float(value) if value else None


class Pagination(
    namedtuple('pagination', [
        'previous',
        'limit',
        'page',
        'next'
    ])
):
    @classmethod
    def create_from_json(cls, meta):
        if meta:
            return cls(
                previous=int_or_null(meta['previous']),
                limit=int(meta['limit']),
                page=int(meta['page']),
                next=int_or_null(meta['next'])
            )
        return meta


class Ticker(
    namedtuple('ticker', [
        'high',
        'low',
        'ask',
        'bid',
        'last_price',
        'volume',
        'market',
        'timestamp',
    ])
):
    @classmethod
    def create_from_json(cls, ticker):
        ticker = ticker[0]
        return cls(
            high=float(ticker['high']),
            low=float(ticker['low']),
            ask=float(ticker['ask']),
            bid=float(ticker['bid']),
            last_price=float(ticker['last_price']),
            volume=float(ticker['volume']),
            market=ticker['market'],
            timestamp=parse_iso_datetime(ticker['timestamp']),
        )


class OrderBookEntry(
    namedtuple('book_entry', [
        'price',
        'amount',
        'timestamp',
    ])
):
    @classmethod
    def create_from_json(cls, book_entry):
        return cls(
            price=float(book_entry['price']),
            amount=float(book_entry['amount']),
            timestamp=parse_iso_datetime(book_entry['timestamp'])
        )


class OrderBook(
    namedtuple('order_book', [
        'order_book',
        'pagination',
    ])
):
    @classmethod
    def create_from_json(cls, order_book, pagination):
        return cls(
            order_book=[OrderBookEntry.create_from_json(book_entry)
                        for book_entry in order_book],
            pagination=Pagination.create_from_json(pagination),
        )


class TradesEntry(
    namedtuple('trades_entry', [
        'market_taker',
        'timestamp',
        'price',
        'amount',
        'market',
    ])
):
    @classmethod
    def create_from_json(cls, trades_entry):
        return cls(
            market_taker=trades_entry['market_taker'],
            timestamp=parse_iso_datetime(trades_entry['timestamp']),
            price=float(trades_entry['price']),
            amount=float(trades_entry['amount']),
            market=trades_entry['market'],
        )


class Trades(
    namedtuple('trades', [
        'trades',
        'pagination',
    ])
):
    @classmethod
    def create_from_json(cls, trades, pagination):
        return cls(
            trades=[TradesEntry.create_from_json(trades_entry)
                    for trades_entry in trades],
            pagination=Pagination.create_from_json(pagination),
        )


class WalletBalance(
    namedtuple('wallet_balance', [
        'available',
        'balance',
        'wallet',
    ])
):
    @classmethod
    def create_from_json(cls, balance):
        return cls(
            available=float(balance['available']),
            balance=float(balance['balance']),
            wallet=balance['wallet'],
        )


class Balance(
    namedtuple('balance', [
        'ARS',
        'CLP',
        'ETH',
    ])
):
    @classmethod
    def create_from_json(cls, balance):
        return cls(
            ARS=cls.get_wallet_balance(balance, 'ARS'),
            CLP=cls.get_wallet_balance(balance, 'CLP'),
            ETH=cls.get_wallet_balance(balance, 'ETH'),
        )

    @staticmethod
    def get_wallet_balance(balance, wallet: str):
        wallet = [b for b in balance if b['wallet'] == wallet]
        return WalletBalance.create_from_json(wallet[0]) if wallet else None


class OrderAmount(
    namedtuple('wallet_balance', [
        'original',
        'remaining',
        'executed',
    ])
):
    @classmethod
    def create_from_json(cls, amount):
        return cls(
            original=float(amount['original']),
            remaining=float_or_null(amount.get('remaining')),
            executed=float_or_null(amount.get('executed')),
        )


class Order(
    namedtuple('order', [
        'id',
        'status',
        'type',
        'price',
        'amount',
        'execution_price',
        'avg_execution_price',
        'market',
        'created_at',
        'updated_at',
        'executed_at',
    ])
):
    @classmethod
    def create_from_json(cls, order):
        return cls(
            # Order ID
            id=order['id'],
            # Order status, 'active' or 'executed'
            status=order['status'],
            # Order type, 'buy' or 'sell'
            type=order['type'],
            # Order limit price
            price=float(order['price']),
            # Order amount
            amount=OrderAmount.create_from_json(order['amount']),
            # Order execution price
            execution_price=float_or_null(
                order.get('execution_price')),
            # Order weighted average execution, 0 if not executed
            avg_execution_price=float_or_null(
                order.get('avg_execution_price')),
            # Market pair
            market=order['market'],
            # Order creation timestamp
            created_at=parse_iso_datetime(order['created_at']),
            # Order update timestamp. Only on active orders
            updated_at=parse_iso_datetime(order.get('created_at')),
            # Order execution timestamp. Only on executed orders
            executed_at=parse_iso_datetime(order.get('executed_at')),
        )


class Orders(
    namedtuple('orders', [
        'orders',
        'pagination',
    ])
):
    @classmethod
    def create_from_json(cls, orders, pagination):
        return cls(
            orders=[Order.create_from_json(order) for order in orders],
            pagination=Pagination.create_from_json(pagination),
        )
