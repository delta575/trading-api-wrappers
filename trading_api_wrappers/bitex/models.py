from collections import namedtuple


class Ticker(
    namedtuple(
        "ticker",
        [
            "last",
            "price_before_last",
            "open",
            "high",
            "low",
            "vwap",
            "volume",
            "bid",
            "ask",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, ticker):
        return cls(
            last=ticker["last"],
            price_before_last=ticker["price_before_last"],
            open=ticker["open"],
            high=ticker["high"],
            low=ticker["low"],
            vwap=ticker["vwap"],
            volume=ticker["volume"],
            bid=ticker["bid"],
            ask=ticker["ask"],
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
                OrderBookEntry.create_from_json(entry) for entry in order_book["asks"]
            ],
            bids=[
                OrderBookEntry.create_from_json(entry) for entry in order_book["bids"]
            ],
            json=order_book,
        )


class Transaction(
    namedtuple(
        "transaction",
        [
            "timestamp",
            "id",
            "price",
            "amount",
        ],
    )
):
    @classmethod
    def create_from_json(cls, transaction):
        return cls(
            timestamp=transaction[0],
            id=transaction[1],
            price=transaction[2],
            amount=transaction[3],
        )
