from . import models as _m
from ..base import Client, ModelMixin


class RipioExchangePublic(Client, ModelMixin):
    """API Doc: https://www.ripio.com/docs/#ripio-exchange"""

    base_url = "https://exchange.ripio.com/api/v1/"
    error_keys = ["detail"]

    def order_books(self):
        """Fetch order books for all markets"""
        data = self.get("book/")
        if self.return_json:
            return data
        return {
            market: _m.OrderBook.create_from_json(book) for market, book in data.items()
        }

    def order_book(self, market: str):
        """Fetch order book for the provided market"""
        data = self.order_books()
        return data[market]


# TODO: Ripio Auth not implemented
class RipioExchangeAuth(RipioExchangePublic):
    def trades(self, page: int = None):
        """Fetch last trades"""
        data = self.get(
            "trades/",
            params={
                "page": page,
            },
        )
        if self.return_json:
            return data
        return _m.Trades.create_from_json(data)


class RipioPublic(Client, ModelMixin):
    """API Doc: https://www.ripio.com/docs/#transactions"""

    base_url = "https://ripio.com/api/v1/"
    error_keys = ["detail"]

    def __init__(self, timeout: int = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self.exchange = RipioExchangePublic(timeout, **kwargs)

    def rates_raw(self):
        return self.get("rates/")

    def rates(self):
        """Fetch rates"""
        data = self.rates_raw()
        data = {"base": data["base"], "rates": data["rates"]}
        if self.return_json:
            return data
        return _m.Rates.create_from_json(data)

    def variation(self):
        """Fetch rates variation"""
        data = self.rates_raw()
        return data["variation"]
