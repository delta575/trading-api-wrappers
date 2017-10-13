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
        data = self.get(url)['data']
        return data

    def ticker(self, market_id: _c.Market):
        url = self.url_for(_p.TICKER)
        params = {
            'market':  _c.Market.check(market_id).value
        }
        data = self.get(url, params=params)['data']
        return _m.Ticker.create_from_json(data)

    def order_book(self,
                   market_id: _c.Market,
                   book_side: _c.OrderBook,
                   page: int=None,
                   limit: int=None):
        params = {
            'market': _c.Market.check(market_id).value,
            'type': _c.OrderBook.check(book_side).value,
            'page': page,
            'limit': limit
        }
        url = self.url_for(_p.ORDER_BOOK)
        data = self.get(url, params=params)
        return _m.OrderBook.create_from_json(data['data'], data['pagination'])

    def trades(self,
               market_id: _c.Market,
               start: str=None,
               end: str=None,
               page: int=None,
               limit: int=None):
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
