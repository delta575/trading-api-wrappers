from collections import namedtuple
from datetime import datetime


def parse_datetime(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def float_or_none(value):
    if value in (None, ""):
        return None
    return float(value)


class Market(
    namedtuple(
        "market",
        [
            "id",
            "base_currency",
            "quote_currency",
            "status",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, symbol, market):
        return cls(
            id=symbol,
            base_currency=market.get("base_currency"),
            quote_currency=market.get("quote_currency"),
            status=market.get("status"),
            json=market,
        )


class Ticker(
    namedtuple(
        "ticker",
        [
            "symbol",
            "ask",
            "bid",
            "last",
            "low",
            "high",
            "open",
            "volume",
            "volume_quote",
            "timestamp",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, symbol, ticker):
        return cls(
            symbol=symbol,
            ask=float_or_none(ticker.get("ask")),
            bid=float_or_none(ticker.get("bid")),
            last=float_or_none(ticker.get("last")),
            low=float_or_none(ticker.get("low")),
            high=float_or_none(ticker.get("high")),
            open=float_or_none(ticker.get("open")),
            volume=float_or_none(ticker.get("volume")),
            volume_quote=float_or_none(ticker.get("volume_quote")),
            timestamp=parse_datetime(ticker.get("timestamp")),
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
        return cls(price=float(book_entry[0]), amount=float(book_entry[1]))


class OrderBook(
    namedtuple(
        "order_book",
        [
            "bids",
            "asks",
            "timestamp",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, order_book):
        return cls(
            bids=[
                OrderBookEntry.create_from_json(entry)
                for entry in order_book.get("bid") or []
            ],
            asks=[
                OrderBookEntry.create_from_json(entry)
                for entry in order_book.get("ask") or []
            ],
            timestamp=parse_datetime(order_book.get("timestamp")),
            json=order_book,
        )


class Trade(
    namedtuple(
        "trade",
        [
            "id",
            "price",
            "quantity",
            "side",
            "timestamp",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, trade):
        return cls(
            id=trade.get("id"),
            price=float_or_none(trade.get("price")),
            quantity=float_or_none(trade.get("qty")),
            side=trade.get("side"),
            timestamp=parse_datetime(trade.get("timestamp")),
            json=trade,
        )


class WalletBalance(
    namedtuple(
        "wallet_balance",
        [
            "currency",
            "available",
            "reserved",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, balance):
        return cls(
            currency=balance.get("currency"),
            available=float_or_none(balance.get("available")),
            reserved=float_or_none(balance.get("reserved")),
            json=balance,
        )


class Order(
    namedtuple(
        "order",
        [
            "id",
            "client_order_id",
            "symbol",
            "side",
            "status",
            "type",
            "quantity",
            "price",
            "created_at",
            "json",
        ],
    )
):
    @classmethod
    def create_from_json(cls, order):
        return cls(
            id=order.get("id"),
            client_order_id=order.get("client_order_id"),
            symbol=order.get("symbol"),
            side=order.get("side"),
            status=order.get("status"),
            type=order.get("type"),
            quantity=float_or_none(order.get("quantity")),
            price=float_or_none(order.get("price")),
            created_at=parse_datetime(order.get("created_at")),
            json=order,
        )
