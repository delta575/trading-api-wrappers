from datetime import datetime

# local
from . import constants as _c
from . import models as _m
from ..base import Client
from .server import CryptoMKTServer

_p = _c.Path


class CryptoMKTPublic(Client):

    error_key = 'message'

    def __init__(self, timeout=30):
        Client.__init__(self, CryptoMKTServer(), timeout)

    def markets(self):
        url = self.url_for(_p.MARKETS)
        data = self.get(url)
        return data['data']

    def ticker(self, market_id: _c.Market):
        url = self.url_for(_p.TICKER)
        params = {
            'market': _c.Market.check(market_id).value
        }
        data = self.get(url, params=params)
        return _m.Ticker.create_from_json(data['data'])

    def order_book(self,
                   market_id: _c.Market,
                   order_type: _c.OrderType,
                   page: int=None,
                   limit: int=_c.ORDERS_LIMIT):
        params = {
            'market': _c.Market.check(market_id).value,
            'type': _c.OrderType.check(order_type).value,
            'page': page,
            'limit': limit
        }
        url = self.url_for(_p.ORDER_BOOK)
        data = self.get(url, params=params)
        return _m.OrderBook.create_from_json(
            data['data'], data['pagination'])

    def trades(self,
               market_id: _c.Market,
               start: datetime=None,
               end: datetime=None,
               page: int=None,
               limit: int=_c.ORDERS_LIMIT):
        if isinstance(start, datetime):
            start = start.strftime('%Y-%m-%d')
        if isinstance(end, datetime):
            end = end.strftime('%Y-%m-%d')
        params = {
            'market': _c.Market.check(market_id).value,
            'start': start,
            'end': end,
            'page': page,
            'limit': limit
        }
        url = self.url_for(_p.TRADES)
        data = self.get(url, params=params)
        return _m.Trades.create_from_json(
            data['data'], data.get('pagination'))
