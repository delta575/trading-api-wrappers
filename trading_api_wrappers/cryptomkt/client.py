# local
from . import constants as _c
from . import models as _m
from ..base import Client
from .server import CryptoMKTServer

_p = _c.Path


class CryptoMKTPublic(Client):
    def __init__(self, timeout=30):
        Client.__init__(self, CryptoMKTServer(), timeout)

    def prices(self,
               market_id: _c.Market,
               time_frame: _c.TimeFrame):
        market_id = _c.Market.check(market_id).value
        time_frame = _c.TimeFrame.check(time_frame).value
        path_arg = (market_id, time_frame)
        url, path = self.url_path_for(_p.PRICES, path_arg=path_arg)
        data = self.get(url)['data']
        return _m.PriceCandles.create_from_json(data)

    def last_prices(self,
                    market_id: _c.Market,
                    time_frame: _c.TimeFrame = _c.TimeFrame.MINUTES_1):
        prices = self.prices(market_id, time_frame)
        return _m.LastPriceCandle.create_from_data(prices)
