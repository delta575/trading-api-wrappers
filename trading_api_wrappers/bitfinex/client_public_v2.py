from datetime import datetime
# local
from . import constants_v2 as _c
from . import models_v2 as _m
from ..base import Client
from .server import BitfinexServerV2 as Server

_p = _c.Path


class BitfinexPublic(Client):
    def __init__(self, timeout=30):
        Client.__init__(self, Server(), timeout)

    def ticker(self, symbol: _c.Symbol = _c.Symbol.BTCUSD):
        symbol = _c.Symbol.check(symbol).value
        url = self.url_for(_p.TICKER, path_arg=symbol)
        data = self.get(url)
        return _m.TradingTicker.create_from_json(data)

    def tickers(self, symbols: list):
        symbols = [_c.Symbol.check(symbol).value for symbol in symbols]
        parameters = {
            'symbols': symbols,
        }
        url = self.url_for(_p.TICKERS)
        data = self.get(url, params=parameters)
        return {ticker[0]: _m.TradingTicker.create_from_json(ticker[1:])
                for ticker in data}

    def trades(self,
               symbol: _c.Symbol = _c.Symbol.BTCUSD,
               limit=None,
               start=None,
               end=None,
               sort=None):
        symbol = _c.Symbol.check(symbol).value
        if isinstance(start, datetime):
            start = start.timestamp() * 1000
        if isinstance(end, datetime):
            end = end.timestamp() * 1000
        if sort:
            sort = 1 if sort is True else -1
        parameters = {
            'limit': limit,
            'start': start,
            'end': end,
            'sort': sort,
        }
        url = self.url_for(_p.TRADES, path_arg=symbol)
        data = self.get(url, params=parameters)
        return [_m.TradingTrade.create_from_json(trade)
                for trade in data]

    def books(self,
              symbol: _c.Symbol,
              precision: _c.BookPrecision,
              length=None):
        symbol = _c.Symbol.check(symbol).value
        precision = _c.BookPrecision.check(precision).value
        parameters = {
            'len': length,
        }
        path_arg = '{0}/{1}'.format(symbol, precision)
        url = self.url_for(_p.BOOKS, path_arg=path_arg)
        data = self.get(url, params=parameters)
        return [_m.TradingBook.create_from_json(book)
                for book in data]

    def stats(self,
              symbol: _c.Symbol,
              key: str,
              size: str,
              side: str,
              section: str,
              sort=None):
        symbol = _c.Symbol.check(symbol).value
        assert key in ['funding.size', 'credits.size', 'credits.size.sym', 'pos.size']
        assert size in ['1m']
        assert side in ['long', 'short']
        assert section in ['last', 'hist']
        if sort:
            sort = 1 if sort is True else -1
        parameters = {
            'sort': sort,
        }
        path_arg = '{0}:{1}:{2}:{3}/{4}'.format(key, size, symbol, side, section)
        url = self.url_for(_p.STATS, path_arg=path_arg)
        data = self.get(url, params=parameters)
        if section == 'last':
            return _m.Stat.create_from_json(data)
        else:
            return [_m.Stat.create_from_json(stat)
                    for stat in data]

    def stats_last(self,
                   symbol: _c.Symbol,
                   key: str,
                   size: str,
                   side: str,
                   sort=None):
        return self.stats(symbol, key, size, side, 'last', sort)

    def stats_hist(self,
                   symbol: _c.Symbol,
                   key: str,
                   size: str,
                   side: str,
                   sort=None):
        return self.stats(symbol, key, size, side, 'hist', sort)

    def candles(self,
                symbol: _c.Symbol,
                section: str,
                time_frame: str,
                limit=None,
                start=None,
                end=None,
                sort=None):
        symbol = _c.Symbol.check(symbol).value
        assert time_frame in ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '7D', '14D', '1M']
        assert section in ['last', 'hist']
        if isinstance(start, datetime):
            start = start.timestamp() * 1000
        if isinstance(end, datetime):
            end = end.timestamp() * 1000
        if sort:
            sort = 1 if sort is True else -1
        parameters = {
            'limit': limit,
            'start': start,
            'end': end,
            'sort': sort,
        }
        path_arg = '{0}:{1}/{2}'.format(time_frame, symbol, section)
        url = self.url_for(_p.CANDLES, path_arg=path_arg)
        data = self.get(url, params=parameters)
        if section == 'last':
            return _m.Candle.create_from_json(data)
        else:
            return [_m.Candle.create_from_json(candle)
                    for candle in data]

    def candles_last(self,
                     symbol: _c.Symbol,
                     time_frame: str,
                     limit=None,
                     start=None,
                     end=None,
                     sort=None):
        return self.candles(symbol, 'last', time_frame, limit, start, end, sort)

    def candles_hist(self,
                     symbol: _c.Symbol,
                     time_frame: str,
                     limit=None,
                     start=None,
                     end=None,
                     sort=None):
        return self.candles(symbol, 'hist', time_frame, limit, start, end, sort)
