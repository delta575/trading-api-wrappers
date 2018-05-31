from datetime import datetime

# local
from . import models_v2 as _m
from .server import BitfinexServer as Server
from ..base import Client


class BitfinexPublic(Client):

    def __init__(self, timeout=30, return_json=False, retry=None):
        super().__init__(Server(version=2), timeout, retry)
        self.return_json = return_json

    def ticker(self, symbol: str):
        url = self.url_for('ticker/%s', symbol)
        data = self.get(url)
        if self.return_json:
            return data
        return _m.TradingTicker.create_from_json(data)

    def tickers(self, symbols: list):
        symbols = [str(symbol) for symbol in symbols]
        params = {
            'symbols': symbols,
        }
        url = self.url_for('tickers')
        data = self.get(url, params=params)
        if self.return_json:
            return data
        return {ticker[0]: _m.TradingTicker.create_from_json(ticker[1:])
                for ticker in data}

    def trades(self,
               symbol: str,
               limit: int=None,
               start: float=None,
               end: float=None,
               sort: bool=None):
        if isinstance(start, datetime):
            start = start.timestamp() * 1000
        if isinstance(end, datetime):
            end = end.timestamp() * 1000
        if sort:
            sort = 1 if sort is True else -1
        params = {
            'limit': limit,
            'start': start,
            'end': end,
            'sort': sort,
        }
        url = self.url_for('trades/%s/hist', symbol)
        data = self.get(url, params=params)
        if self.return_json:
            return data
        return [_m.TradingTrade.create_from_json(trade)
                for trade in data]

    def books(self,
              symbol: str,
              precision: str,
              length: int=None):
        params = {
            'len': length,
        }
        path_arg = f'{symbol}/{precision}'
        url = self.url_for('book/%s', path_arg)
        data = self.get(url, params=params)
        if self.return_json:
            return data
        return [_m.TradingBook.create_from_json(book)
                for book in data]

    def stats(self,
              symbol: str,
              key: str,
              size: str,
              side: str,
              section: str,
              sort: bool=None):
        if sort:
            sort = 1 if sort else -1
        params = {
            'sort': sort,
        }
        path_arg = f'{key}:{size}:{symbol}:{side}/{section}'
        url = self.url_for('stats1/%s', path_arg)
        data = self.get(url, params=params)
        if self.return_json:
            return data
        if section == 'last':
            return _m.Stat.create_from_json(data)
        else:
            return [_m.Stat.create_from_json(stat)
                    for stat in data]

    def stats_last(self,
                   symbol: str,
                   key: str,
                   size: str,
                   side: str,
                   sort: bool=None):
        return self.stats(symbol, key, size, side, 'last', sort)

    def stats_hist(self,
                   symbol: str,
                   key: str,
                   size: str,
                   side: str,
                   sort: bool=None):
        return self.stats(symbol, key, size, side, 'hist', sort)

    def candles(self,
                symbol: str,
                section: str,
                time_frame: str,
                limit: int=None,
                start: float=None,
                end: float=None,
                sort: bool=None):
        if isinstance(start, datetime):
            start = start.timestamp() * 1000
        if isinstance(end, datetime):
            end = end.timestamp() * 1000
        if sort:
            sort = 1 if sort else -1
        params = {
            'limit': limit,
            'start': start,
            'end': end,
            'sort': sort,
        }
        path_arg = f'{time_frame}:{symbol}/{section}'
        url = self.url_for('candles/trade:%s', path_arg)
        data = self.get(url, params=params)
        if self.return_json:
            return data
        if section == 'last':
            return _m.Candle.create_from_json(data)
        else:
            return [_m.Candle.create_from_json(candle)
                    for candle in data]

    def candles_last(self,
                     symbol: str,
                     time_frame: str,
                     limit: int=None,
                     start: float=None,
                     end: float=None,
                     sort: bool=None):
        return self.candles(
            symbol, 'last', time_frame, limit, start, end, sort)

    def candles_hist(self,
                     symbol: str,
                     time_frame: str,
                     limit: int=None,
                     start: float=None,
                     end: float=None,
                     sort: bool=None):
        return self.candles(
            symbol, 'hist', time_frame, limit, start, end, sort)
