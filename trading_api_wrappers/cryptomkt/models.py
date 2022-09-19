from collections import namedtuple
from datetime import datetime


def parse_datetime(datetime_str):
    if datetime_str:
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")


def parse_iso_datetime(datetime_str):
    if datetime_str:
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")


def check_null(value):
    return value if value != "null" else None


def int_or_null(value):
    value = check_null(value)
    return int(value) if value else None


def float_or_null(value):
    value = check_null(value)
    return float(value) if value else None


class Pagination(namedtuple("pagination", ["previous", "limit", "page", "next"])):
    @classmethod
    def create_from_json(cls, meta):
        if meta:
            return cls(
                previous=int_or_null(meta["previous"]),
                limit=int(meta["limit"]),
                page=int(meta["page"]),
                next=int_or_null(meta["next"]),
            )
        return meta


class Ticker(
    namedtuple(
        "ticker",
        [
            "high",
            "low",
            "ask",
            "bid",
            "last_price",
            "volume",
            "market",
            "timestamp",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, ticker):
        ticker = ticker[0]
        return cls(
            high=float(ticker.get("high")),
            low=float(ticker.get("low")),
            ask=float(ticker.get("ask")),
            bid=float(ticker.get("bid")),
            last_price=float(ticker.get("last_price", ticker["last"])),
            volume=float(ticker.get("volume")),
            market=ticker.get("market"),
            timestamp=parse_iso_datetime(ticker.get("timestamp")),
            json=ticker,
        )


class OrderBookEntry(
    namedtuple(
        "book_entry",
        [
            "price",
            "amount",
        ],
    )
):
    @classmethod
    def create_from_json(cls, book_entry):
        return cls(
            price=float(book_entry[0]),
            amount=float(book_entry[1]),
        )


class OrderBook(
    namedtuple(
        "order_book",
        [
            "asks",
            "bids",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, order_book):
        return cls(
            asks=[
                OrderBookEntry.create_from_json(entry) for entry in order_book["ask"]
            ],
            bids=[
                OrderBookEntry.create_from_json(entry) for entry in order_book["bid"]
            ],
            json=order_book,
        )

class TradesEntry(
    namedtuple(
        "trades_entry",
        [
            "id",
            "price",
            "qty",
            "side",
            "timestamp",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, trades_entry):
        return cls(
            id= trades_entry["id"],
            price= float(trades_entry["price"]),
            qty= float(trades_entry["qty"]),
            side= trades_entry["side"],
            timestamp= parse_iso_datetime(trades_entry["timestamp"]),
            json=trades_entry,
        )


class Trades(
    namedtuple(
        "trades",
        [
            "trades",
        ],
    )
):
    @classmethod
    def create_from_json(cls, trades):
        return cls(
            trades=[
                TradesEntry.create_from_json(trades_entry) for trades_entry in trades
            ],
        )


class WalletBalance(
    namedtuple(
        "wallet_balance",
        [
            "available",
            "balance",
            "wallet",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, balance):
        return cls(
            available=float(balance["available"]),
            balance=float(balance["balance"]),
            wallet=balance["wallet"],
            json=balance,
        )


class Balance(
    namedtuple(
        "balance",
        [
            "ARS",
            "CLP",
            "ETH",
        ],
    )
):
    @classmethod
    def create_from_json(cls, balance):
        return cls(
            ARS=cls.get_wallet_balance(balance, "ARS"),
            CLP=cls.get_wallet_balance(balance, "CLP"),
            ETH=cls.get_wallet_balance(balance, "ETH"),
        )

    @staticmethod
    def get_wallet_balance(balance, wallet: str):
        wallet = [b for b in balance if b["wallet"] == wallet]
        return WalletBalance.create_from_json(wallet[0]) if wallet else None


class OrderAmount(
    namedtuple(
        "wallet_balance",
        [
            "original",
            "remaining",
            "executed",
        ],
    )
):
    @classmethod
    def create_from_json(cls, amount):
        return cls(
            original=float(amount["original"]),
            remaining=float_or_null(amount.get("remaining")),
            executed=float_or_null(amount.get("executed")),
        )


class Order(
    namedtuple(
        "order",
        [
            "id",
            "status",
            "type",
            "price",
            "amount",
            "execution_price",
            "avg_execution_price",
            "market",
            "created_at",
            "updated_at",
            "executed_at",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, order):
        return cls(
            # Order ID
            id=order["id"],
            # Order status, 'active' or 'executed'
            status=order["status"],
            # Order type, 'buy' or 'sell'
            type=order["type"],
            # Order limit price
            price=float(order["price"]),
            # Order amount
            amount=OrderAmount.create_from_json(order["amount"]),
            # Order execution price
            execution_price=float_or_null(order.get("execution_price")),
            # Order weighted average execution, 0 if not executed
            avg_execution_price=float_or_null(order.get("avg_execution_price")),
            # Market pair
            market=order["market"],
            # Order creation timestamp
            created_at=parse_iso_datetime(order["created_at"]),
            # Order update timestamp. Only on active orders
            updated_at=parse_iso_datetime(order.get("created_at")),
            # Order execution timestamp. Only on executed orders
            executed_at=parse_iso_datetime(order.get("executed_at")),
            # Order JSON data
            json=order,
        )


class Orders(
    namedtuple(
        "orders",
        [
            "orders",
            "pagination",
        ],
    )
):
    @classmethod
    def create_from_json(cls, orders, pagination):
        return cls(
            orders=[Order.create_from_json(order) for order in orders],
            pagination=Pagination.create_from_json(pagination),
        )
