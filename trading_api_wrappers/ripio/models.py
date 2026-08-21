from collections import namedtuple
from datetime import datetime


def parse_datetime(datetime_str):
    if datetime_str:
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")


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
            price=float(book_entry["price"]),
            amount=float(book_entry["amount"]),
        )


class OrderBook(
    namedtuple(
        "order_book",
        [
            "bids",
            "asks",
            "timestamp",
            "hash",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, order_book):
        return cls(
            bids=[
                OrderBookEntry.create_from_json(book_entry)
                for book_entry in order_book.get("bids") or []
            ],
            asks=[
                OrderBookEntry.create_from_json(book_entry)
                for book_entry in order_book.get("asks") or []
            ],
            timestamp=order_book.get("timestamp"),
            hash=order_book.get("hash"),
            json=order_book,
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
