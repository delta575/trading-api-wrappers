from collections import namedtuple
from datetime import datetime


def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

def parse_iso_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f')

def int_or_null(value):
    return int(value) if value != 'null' else None


class Pagination(
    namedtuple('pagination', [
        'previous',
        'limit',
        'page',
        'next'
    ])
):

    @classmethod
    def create_from_json(cls, meta):
        if meta:
            return cls(
                previous=int_or_null(meta['previous']),
                limit=int(meta['limit']),
                page=int(meta['page']),
                next=int_or_null(meta['next'])
            )
        return meta


class PriceCandle(
    namedtuple('price', [
        'candle_id',
        'open_price',
        'high_price',
        'low_price',
        'close_price',
        'volume_sum',
        'candle_date',
        'tick_count',
    ])
):
    @classmethod
    def create_from_json(cls, price):
        return cls(
            candle_id=int(price['candle_id']),
            open_price=float(price['open_price']),
            high_price=float(price['hight_price']),  # Typo in API
            low_price=float(price['low_price']),
            close_price=float(price['close_price']),
            volume_sum=float(price['volume_sum']),
            candle_date=parse_datetime(price['candle_date']),
            tick_count=int(price['tick_count']),
        )


class PriceCandles(
    namedtuple('prices', [
        'asks',
        'bids',
    ])
):
    @classmethod
    def create_from_json(cls, prices):
        return cls(
            asks=[PriceCandle.create_from_json(value)
                  for value in prices['prices_ask']['values']],
            bids=[PriceCandle.create_from_json(entry)
                  for entry in prices['prices_bid']['values']],
        )


class LastPriceCandle(
    namedtuple('last_price', [
        'ask',
        'bid',
    ])
):
    @classmethod
    def create_from_data(cls, prices: PriceCandles):
        return cls(
            ask=prices.asks[1],
            bid=prices.bids[1],
        )


class Ticker(
    namedtuple('ticker', [
        'high',
        'low',
        'ask',
        'bid',
        'last_price',
        'volume',
        'market',
        'timestamp'
    ])
):

    @classmethod
    def create_from_json(cls, ticker):
        return cls(
            high=float(ticker[0]['high']),
            low=float(ticker[0]['low']),
            ask=float(ticker[0]['ask']),
            bid=float(ticker[0]['bid']),
            last_price=float(ticker[0]['last_price']),
            volume=float(ticker[0]['volume']),
            market=ticker[0]['market'],
            timestamp=parse_iso_datetime(ticker[0]['timestamp'])
        )

class OrderBookEntry(
    namedtuple('book_entry', [
        'price',
        'amount',
        'timestamp'
    ])
):
    @classmethod
    def create_from_json(cls, book_entry):
        return cls(
            price=float(book_entry['price']),
            amount=float(book_entry['amount']),
            timestamp=parse_iso_datetime(book_entry['timestamp'])
        )


class OrderBook(
    namedtuple('order_book', [
        'order_book',
        'pagination',
    ])
):

    @classmethod
    def create_from_json(cls, book, pagination):
        return cls(
            order_book=[OrderBookEntry.create_from_json(book_entry)
                        for book_entry in book],
            pagination=Pagination.create_from_json(pagination),
        )

class TradesEntry(
    namedtuple('trades_entry', [
        'market_taker',
        'timestamp',
        'price',
        'amount',
        'market'
    ])
):
    @classmethod
    def create_from_json(cls, trades_entry):
        return cls(
            market_taker=trades_entry['market_taker'],
            timestamp=parse_iso_datetime(trades_entry['timestamp']),
            price=float(trades_entry['price']),
            amount=float(trades_entry['amount']),
            market=trades_entry['market']
        )


class Trades(
    namedtuple('trades', [
        'trades',
        'pagination',
    ])
):

    @classmethod
    def create_from_json(cls, trades, pagination):
        return cls(
            trades=[TradesEntry.create_from_json(trades_entry)
                        for trades_entry in trades],
            pagination=Pagination.create_from_json(pagination),
        )