from collections import namedtuple


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
            "exchange",
        ],
    )
):
    @classmethod
    def create_from_json(cls, book_entry):
        return cls(
            price=float(book_entry[0]),
            amount=float(book_entry[1]),
            exchange=book_entry[2],
        )


class OrderBook(
    namedtuple(
        "order_book",
        [
            "bids",
            "asks",
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
            json=order_book,
        )
