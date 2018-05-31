from datetime import datetime

# local
from . import constants as _c
from . import models as _m
from ..base import Client
from .server import CryptoMKTServer


class CryptoMKTPublic(Client):

    error_key = 'message'

    def __init__(self, timeout: int=30, return_json=False, retry=None):
        super().__init__(CryptoMKTServer(), timeout, retry)
        self.return_json = return_json

    def markets(self):
        url = self.url_for('market')
        data = self.get(url)
        return data['data']

    def ticker(self, market_id: str):
        url = self.url_for('ticker')
        params = {
            'market': str(market_id)
        }
        data = self.get(url, params=params)
        if self.return_json:
            return data
        return _m.Ticker.create_from_json(data['data'])

    def order_book(self,
                   market_id: str,
                   order_type: str,
                   page: int=None,
                   limit: int=_c.ORDERS_LIMIT):
        params = {
            'market': str(market_id),
            'type': str(order_type),
            'page': page,
            'limit': limit
        }
        url = self.url_for('book')
        data = self.get(url, params=params)
        if self.return_json:
            return data
        return _m.OrderBook.create_from_json(
            data['data'], data['pagination'])

    def trades(self,
               market_id: str,
               start: datetime=None,
               end: datetime=None,
               page: int=None,
               limit: int=_c.ORDERS_LIMIT):
        if isinstance(start, datetime):
            start = start.strftime('%Y-%m-%d')
        if isinstance(end, datetime):
            end = end.strftime('%Y-%m-%d')
        params = {
            'market': str(market_id),
            'start': start,
            'end': end,
            'page': page,
            'limit': limit,
        }
        url = self.url_for('trades')
        data = self.get(url, params=params)
        if self.return_json:
            return data
        return _m.Trades.create_from_json(
            data['data'], data.get('pagination'))
