from . import constants as _c
from . import models as _m
from ..base import Client, ModelMixin


class SFOXPublic(Client, ModelMixin):
    """API Doc: https://www.sfox.com/developers"""

    base_url = "https://api.sfox.com/v1/"

    def best_price(self, side: str, amount: str):
        """Return the price needed for a limit order to execute fully."""
        data = self.get(f"offer/{side}", params={"amount": amount})
        if self.return_json:
            return data
        return _m.Price.create_from_json(data)

    def best_buy_price(self, amount: str):
        """Return the price needed for a limit BUY order to execute fully."""
        return self.best_price(_c.Side.BUY.value, amount)

    def best_sell_price(self, amount: str):
        """Return the price needed for a limit SELL order to execute fully."""
        return self.best_price(_c.Side.SELL.value, amount)

    def order_book_raw(self):
        return self.get("markets/orderbook")

    def order_book(self, market_making: bool = False):
        """Return the blended order book of all the available exchanges."""
        data = self.order_book_raw()
        if market_making:
            data = data["market_making"]
        order_book = {"bids": data["bids"], "asks": data["asks"]}
        if self.return_json:
            return order_book
        return _m.OrderBook.create_from_json(order_book)

    def market_making_order_book(self):
        """Return the blended market making order book of all the available
        exchanges."""
        return self.order_book(market_making=True)

    def exchanges(self):
        """Return all the available exchanges."""
        data = self.order_book_raw()
        return data["exchanges"]
