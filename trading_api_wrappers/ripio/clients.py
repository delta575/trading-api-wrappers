
from ..base import Client, ModelMixin
from ..errors import InvalidResponse
from . import models as _m


class RipioExchangePublic(Client, ModelMixin):
    """Ripio Trade public REST API (v4)."""

    base_url = "https://api.ripiotrade.co/v4/"
    error_keys = ["message"]

    def _decode_response(self, response):
        payload = super()._decode_response(response)
        if isinstance(payload, dict) and "data" in payload:
            if payload.get("error_code"):
                raise InvalidResponse(payload.get("message") or str(payload["error_code"]), response)
            return payload["data"]
        return payload

    def pairs(self):
        return self.get("public/pairs")

    def tickers(self):
        return self.get("public/tickers")

    def ticker(self, pair: str):
        pair = str(pair)
        for item in self.tickers():
            if item.get("pair") == pair:
                return item
        raise KeyError(pair)

    def order_books(self):
        """Return tickers for all pairs (Trade API has no bulk order-book)."""
        return {item["pair"]: item for item in self.tickers()}

    def order_book(self, pair: str, limit: int | None = None):
        data = self.get(
            "public/orders/level-2",
            params={"pair": str(pair), "limit": limit},
        )
        if self.return_json:
            return data
        return _m.OrderBook.create_from_json(data)


class RipioPublic(Client, ModelMixin):
    """Ripio retail rates API."""

    base_url = "https://ripio.com/api/v1/"
    error_keys = ["detail"]

    def __init__(self, timeout: int | None = None, **kwargs):
        super().__init__(timeout, **kwargs)
        self._exchange = None
        self._timeout = timeout
        self._kwargs = kwargs

    @property
    def exchange(self):
        if self._exchange is None:
            self._exchange = RipioExchangePublic(self._timeout, **self._kwargs)
        return self._exchange

    def rates_raw(self):
        return self.get("rates/")

    def rates(self):
        data = self.rates_raw()
        data = {"base": data["base"], "rates": data["rates"]}
        if self.return_json:
            return data
        return _m.Rates.create_from_json(data)

    def variation(self):
        data = self.rates_raw()
        return data["variation"]
