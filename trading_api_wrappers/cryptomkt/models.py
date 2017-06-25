from collections import namedtuple
from datetime import datetime


def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')


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
