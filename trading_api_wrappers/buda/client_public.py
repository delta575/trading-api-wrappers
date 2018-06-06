# local
from . import constants as _c
from . import models as _m
from ..base import Client
from .server import BudaServer


class BudaPublic(Client):

    error_key = 'message'

    def __init__(self, timeout: int=30, host: str=None,
                 return_json: bool=False, retry=None):
        super().__init__(BudaServer(host), timeout, retry)
        self.return_json = return_json

    def markets(self):
        url, path = self.url_path_for('markets')
        data = self.get(url)
        if self.return_json:
            return data
        return [_m.Market.create_from_json(market)
                for market in data['markets']]

    def market_details(self, market_id: str):
        url = self.url_for('markets/%s', market_id)
        data = self.get(url)
        if self.return_json:
            return data
        return _m.Market.create_from_json(data['market'])

    def ticker(self, market_id: str):
        url = self.url_for('markets/%s/ticker', market_id)
        data = self.get(url)
        if self.return_json:
            return data
        return _m.Ticker.create_from_json(data['ticker'])

    def order_book(self, market_id: str):
        url = self.url_for('markets/%s/order_book', market_id)
        data = self.get(url)
        if self.return_json:
            return data
        return _m.OrderBook.create_from_json(data['order_book'])

    def trades(self,
               market_id: str,
               timestamp: int=None,
               limit: int=None):
        params = {
            'timestamp': timestamp,
            'limit': limit,
        }
        url, path = self.url_path_for('markets/%s/trades', market_id)
        data = self.get(url, params=params)
        if self.return_json:
            return data
        return _m.Trades.create_from_json(data['trades'])
