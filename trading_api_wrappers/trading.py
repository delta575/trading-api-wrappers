"""Shared trading helpers (Buda-style quotation from an order book)."""

from .market import OrderBook, quote_from_book


class BookQuotationMixin:
    """Add ``quotation()`` to any client that already exposes ``order_book``."""

    def quotation(self, symbol, quotation_type, amount, limit=None, **kwargs):
        book = self.order_book(symbol, **kwargs)
        if not hasattr(book, "bids"):
            book = OrderBook.create(book)
        quoted = quote_from_book(book, quotation_type, amount, limit)
        if getattr(self, "return_json", False):
            return quoted.json
        return quoted

    def quotation_market(self, symbol, quotation_type, amount, **kwargs):
        return self.quotation(symbol, quotation_type, amount, limit=None, **kwargs)

    def quotation_limit(self, symbol, quotation_type, amount, limit, **kwargs):
        return self.quotation(symbol, quotation_type, amount, limit=limit, **kwargs)
