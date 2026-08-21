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


def _unwrap_book(data):
    """Accept a raw book or a venue envelope (Kraken ``result``)."""
    if not isinstance(data, dict):
        return {}
    if "bids" in data or "asks" in data or "b" in data or "a" in data:
        return data
    result = data.get("result")
    if isinstance(result, dict):
        for value in result.values():
            if isinstance(value, dict) and (
                "bids" in value or "asks" in value or "b" in value or "a" in value
            ):
                return value
    return data


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
        payload = _unwrap_book(data)
        raw_bids = (
            bids if bids is not None else payload.get("bids") or payload.get("b") or []
        )
        raw_asks = (
            asks if asks is not None else payload.get("asks") or payload.get("a") or []
        )
        ts = (
            timestamp
            if timestamp is not None
            else payload.get("timestamp", payload.get("ts"))
        )
        return cls(
            bids=[OrderBookEntry.create(entry) for entry in raw_bids],
            asks=[OrderBookEntry.create(entry) for entry in raw_asks],
            timestamp=ts,
            json=data,
        )


class Candlestick(
    namedtuple(
        "candlestick",
        [
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "json",
        ],
    )
):
    @classmethod
    def create(
        cls,
        data,
        *,
        timestamp=None,
        open_price=None,
        high=None,
        low=None,
        close=None,
        volume=None,
    ):
        return cls(
            timestamp=timestamp,
            open=_float(open_price),
            high=_float(high),
            low=_float(low),
            close=_float(close),
            volume=_float(volume),
            json=data,
        )


class Quotation(
    namedtuple(
        "quotation",
        [
            "side",
            "base_exchanged",
            "quote_exchanged",
            "average_price",
            "incomplete",
            "json",
        ],
    )
):
    pass


_BUY_TYPES = {
    "bid",
    "buy",
    "bid_given_size",
    "bid_given_earned_base",
    "bid_given_spent_quote",
}
_QUOTE_TYPES = {
    "bid_given_spent_quote",
    "ask_given_earned_quote",
}


def quote_from_book(book, quotation_type, amount, limit=None):
    """Walk an order book the way Buda's quotation endpoint does.

    ``quotation_type`` accepts Buda names (``bid_given_size``,
    ``ask_given_spent_base``, …) or simply ``buy`` / ``sell``.
    """
    qtype = str(quotation_type).lower()
    buy = qtype in _BUY_TYPES or qtype.startswith("bid")
    quote_amount = qtype in _QUOTE_TYPES
    levels = list(book.asks if buy else book.bids)
    reverse = not buy
    levels = sorted(levels, key=lambda entry: float(entry.price), reverse=reverse)

    remaining = float(amount)
    base = 0.0
    quote = 0.0
    limit_px = float(limit) if limit not in (None, "") else None

    for entry in levels:
        price = float(entry.price)
        available = float(entry.amount)
        if limit_px is not None:
            if buy and price > limit_px:
                continue
            if not buy and price < limit_px:
                continue
        if quote_amount:
            take_quote = min(remaining, available * price)
            take_base = take_quote / price if price else 0.0
            remaining -= take_quote
        else:
            take_base = min(remaining, available)
            take_quote = take_base * price
            remaining -= take_base
        base += take_base
        quote += take_quote
        if remaining <= 1e-12:
            remaining = 0.0
            break

    avg = (quote / base) if base else None
    payload = {
        "side": "buy" if buy else "sell",
        "base_exchanged": base,
        "quote_exchanged": quote,
        "average_price": avg,
        "incomplete": remaining > 1e-12,
        "remaining": remaining,
    }
    return Quotation(
        side=payload["side"],
        base_exchanged=base,
        quote_exchanged=quote,
        average_price=avg,
        incomplete=payload["incomplete"],
        json=payload,
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
