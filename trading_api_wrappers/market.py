"""Shared market-data models used by the LATAM and global venue clients."""

from collections import namedtuple


def _float(value):
    if value in (None, ""):
        return None
    return float(value)


def _int(value):
    if value in (None, ""):
        return None
    return int(value)


class Market(
    namedtuple(
        "market",
        [
            "id",
            "base",
            "quote",
            "json",
        ],
    )
):
    @classmethod
    def create(cls, market_id, base=None, quote=None, json=None):
        return cls(
            id=str(market_id),
            base=base,
            quote=quote,
            json=json if json is not None else market_id,
        )


class Ticker(
    namedtuple(
        "ticker",
        [
            "symbol",
            "last",
            "bid",
            "ask",
            "volume",
            "timestamp",
            "json",
        ],
    )
):
    @classmethod
    def create(
        cls,
        data,
        *,
        symbol=None,
        last=None,
        bid=None,
        ask=None,
        volume=None,
        timestamp=None,
    ):
        return cls(
            symbol=symbol,
            last=_float(last),
            bid=_float(bid),
            ask=_float(ask),
            volume=_float(volume),
            timestamp=_int(timestamp) if timestamp not in (None, "") else timestamp,
            json=data,
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
    def create(cls, entry):
        if isinstance(entry, dict):
            price = entry.get("price", entry.get("limitPrice", entry.get("px")))
            amount = entry.get(
                "amount",
                entry.get("qty", entry.get("size", entry.get("volume"))),
            )
            return cls(price=float(price), amount=float(amount))
        return cls(price=float(entry[0]), amount=float(entry[1]))


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
    def create(cls, data, bids=None, asks=None, timestamp=None):
        raw_bids = bids if bids is not None else data.get("bids") or data.get("b") or []
        raw_asks = asks if asks is not None else data.get("asks") or data.get("a") or []
        ts = timestamp if timestamp is not None else data.get("timestamp", data.get("ts"))
        return cls(
            bids=[OrderBookEntry.create(entry) for entry in raw_bids],
            asks=[OrderBookEntry.create(entry) for entry in raw_asks],
            timestamp=ts,
            json=data,
        )


class Trade(
    namedtuple(
        "trade",
        [
            "id",
            "price",
            "amount",
            "side",
            "timestamp",
            "json",
        ],
    )
):
    @classmethod
    def create(
        cls,
        data,
        *,
        trade_id=None,
        price=None,
        amount=None,
        side=None,
        timestamp=None,
    ):
        return cls(
            id=trade_id,
            price=_float(price),
            amount=_float(amount),
            side=side,
            timestamp=timestamp,
            json=data,
        )
