# local
from . import models as _m
from .server import BudaServer
from ..base import Client


class BudaPublic(Client):
    error_key = 'message'

    def __init__(self,
                 timeout: int=30,
                 host: str=None,
                 return_json: bool=False,
                 retry=None):
        super().__init__(BudaServer(host), timeout, retry)
        self.return_json = return_json

    def markets(self):
        data = self.get('markets')
        if self.return_json:
            return data
        return [_m.Market.create_from_json(market)
                for market in data['markets']]

    def market_details(self, market_id: str):
        data = self.get(f'markets/{market_id}')
        if self.return_json:
            return data
        return _m.Market.create_from_json(data['market'])

    def ticker(self, market_id: str):
        data = self.get(f'markets/{market_id}/ticker')
        if self.return_json:
            return data
        return _m.Ticker.create_from_json(data['ticker'])

    def order_book(self, market_id: str):
        data = self.get(f'markets/{market_id}/order_book')
        if self.return_json:
            return data
        return _m.OrderBook.create_from_json(data['order_book'])

    def trades(self,
               market_id: str,
               timestamp: int=None,
               limit: int=None):
        data = self.get(f'markets/{market_id}/trades', params={
            'timestamp': timestamp,
            'limit': limit,
        })
        if self.return_json:
            return data
        return _m.Trades.create_from_json(data['trades'])
