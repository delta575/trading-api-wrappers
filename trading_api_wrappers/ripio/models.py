from collections import namedtuple
from datetime import datetime


def parse_datetime(datetime_str):
    if datetime_str:
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")


class Price(
    namedtuple(
        "price",
        [
            "quantity",
            "vwap",
            "price",
            "fees",
            "total",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, price):
        return cls(
            quantity=float(price["quantity"]),
            vwap=float(price["vwap"]),
            price=float(price["price"]),
            fees=float(price["fees"]),
            total=float(price["total"]),
            json=price,
        )


class OrderBookEntry(
    namedtuple(
        "book_entry",
        [
            "price",
            "amount",
            "orders",
        ],
    )
):
    @classmethod
    def create_from_json(cls, book_entry):
        return cls(
            price=book_entry["price"],
            amount=book_entry["amount"],
            orders=book_entry["orders"],
        )


class OrderBook(
    namedtuple(
        "order_book",
        [
            "bids",
            "asks",
            "timestamp",
            "last_price",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, order_book):
        return cls(
            bids=[
                OrderBookEntry.create_from_json(book_entry)
                for book_entry in order_book["bids"]
            ],
            asks=[
                OrderBookEntry.create_from_json(book_entry)
                for book_entry in order_book["asks"]
            ],
            timestamp=order_book["timestamp"],
            last_price=order_book["last_price"],
            json=order_book,
        )


class Trade(
    namedtuple(
        "trade",
        [
            "id",
            "uuid",
            "engine_id",
            "pair",
            "amount",
            "price",
            "created_at",
        ],
    )
):
    @classmethod
    def create_from_json(cls, trade):
        return cls(
            id=trade["id"],
            uuid=trade["uuid"],
            engine_id=trade["engine_id"],
            pair=trade["pair"],
            amount=trade["amount"],
            price=float(trade["price"]),
            created_at=parse_datetime(trade["created_at"]),
        )


class Trades(
    namedtuple(
        "trades",
        [
            "count",
            "next",
            "previous",
            "results",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, trades):
        return cls(
            count=trades["count"],
            next=trades["next"],
            previous=trades["previous"],
            results=[Trade.create_from_json(trade) for trade in trades["results"]],
            json=trades,
        )


class Rates(
    namedtuple(
        "rates",
        [
            "base",
            "rates",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, rates):
        return cls(
            base=rates["base"],
            rates=rates["rates"],
            json=rates,
        )
