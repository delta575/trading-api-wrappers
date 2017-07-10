# local
from . import constants as _c
from . import models as _m
from ..base import Client
from .server import SURBTCServer

_p = _c.Path


class SURBTCPublic(Client):

    error_key = 'message'

    def __init__(self, test=False, timeout=30):
        Client.__init__(self, SURBTCServer(test), timeout)

    def markets(self):
        url, path = self.url_path_for(_p.MARKETS)
        data = self.get(url)
        return [_m.Market.create_from_json(market)
                for market in data['markets']]

    def market_details(self, market_id: _c.Market):
        market_id = _c.Market.check(market_id)
        url = self.url_for(_p.MARKET_DETAILS, path_arg=market_id.value)
        data = self.get(url)
        return _m.Market.create_from_json(data['market'])

    def ticker(self, market_id: _c.Market):
        market_id = _c.Market.check(market_id)
        url = self.url_for(_p.TICKER, path_arg=market_id.value)
        data = self.get(url)
        return _m.Ticker.create_from_json(data['ticker'])

    def order_book(self, market_id: _c.Market):
        market_id = _c.Market.check(market_id)
        url = self.url_for(_p.ORDER_BOOK, path_arg=market_id.value)
        data = self.get(url)
        return _m.OrderBook.create_from_json(data['order_book'])

    def trade_transaction_pages(self,
                                market_id: _c.Market,
                                page: int=None,
                                per_page: int=None):
        market_id = _c.Market.check(market_id)
        params = {
            'page': page,
            'per': per_page,
        }
        url, path = self.url_path_for(_p.TRADE_TRANSACTIONS,
                                      path_arg=market_id.value)
        data = self.get(url, params=params)
        return _m.TradeTransactionPages.create_from_json(
            data['trade_transactions'], data.get('meta'))
