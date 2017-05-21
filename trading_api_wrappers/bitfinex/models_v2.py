from collections import namedtuple


class TradingTicker(
    namedtuple('trading_ticker', [
        'BID',
        'BID_SIZE',
        'ASK',
        'ASK_SIZE',
        'DAILY_CHANGE',
        'DAILY_CHANGE_PERC',
        'LAST_PRICE',
        'VOLUME',
        'HIGH',
        'LOW',
    ])
):

    @classmethod
    def create_from_json(cls, ticker):
        return cls(
            BID=ticker[0],
            BID_SIZE=ticker[1],
            ASK=ticker[2],
            ASK_SIZE=ticker[3],
            DAILY_CHANGE=ticker[4],
            DAILY_CHANGE_PERC=ticker[5],
            LAST_PRICE=ticker[6],
            VOLUME=ticker[7],
            HIGH=ticker[8],
            LOW=ticker[9],
        )


class FoundingTicker(
    namedtuple('founding_ticker', [
        'FRR',
        'BID',
        'BID_SIZE',
        'BID_PERIOD',
        'ASK',
        'ASK_SIZE',
        'ASK_PERIOD',
        'DAILY_CHANGE',
        'DAILY_CHANGE_PERC',
        'LAST_PRICE',
        'VOLUME',
        'HIGH',
        'LOW',
    ])
):

    @classmethod
    def create_from_json(cls, ticker):
        return cls(
            FRR=ticker[0],
            BID=ticker[1],
            BID_SIZE=ticker[2],
            BID_PERIOD=ticker[3],
            ASK=ticker[4],
            ASK_SIZE=ticker[5],
            ASK_PERIOD=ticker[6],
            DAILY_CHANGE=ticker[7],
            DAILY_CHANGE_PERC=ticker[8],
            LAST_PRICE=ticker[9],
            VOLUME=ticker[10],
            HIGH=ticker[11],
            LOW=ticker[12],
        )


class TradingTrade(
    namedtuple('trading_trade', [
        'ID',
        'MTS',
        'AMOUNT',
        'PRICE',
    ])
):

    @classmethod
    def create_from_json(cls, trade):
        return cls(
            ID=trade[0],
            MTS=trade[1],
            AMOUNT=trade[2],
            PRICE=trade[3],
        )


class FoundingTrade(
    namedtuple('founding_trade', [
        'ID',
        'MTS',
        'AMOUNT',
        'RATE',
        'PERIOD',
    ])
):

    @classmethod
    def create_from_json(cls, trade):
        return cls(
            ID=trade[0],
            MTS=trade[1],
            AMOUNT=trade[2],
            RATE=trade[3],
            PERIOD=trade[4],
        )


class TradingBook(
    namedtuple('trading_book', [
        'PRICE',
        'COUNT',
        'AMOUNT',
    ])
):

    @classmethod
    def create_from_json(cls, book):
        return cls(
            PRICE=book[0],
            COUNT=book[1],
            AMOUNT=book[2],
        )


class FoundingBook(
    namedtuple('founding_book', [
        'RATE',
        'PERIOD',
        'COUNT',
        'AMOUNT',
    ])
):

    @classmethod
    def create_from_json(cls, book):
        return cls(
            RATE=book[0],
            PERIOD=book[1],
            COUNT=book[2],
            AMOUNT=book[3],
        )


class Stat(
    namedtuple('stat', [
        'MTS',
        'VALUE',
    ])
):

    @classmethod
    def create_from_json(cls, stat):
        return cls(
            MTS=stat[0],
            VALUE=stat[1],
        )


class Candle(
    namedtuple('candle', [
        'MTS',
        'OPEN',
        'CLOSE',
        'HIGH',
        'LOW',
        'VOLUME',
    ])
):

    @classmethod
    def create_from_json(cls, candle):
        return cls(
            MTS=candle[0],
            OPEN=candle[1],
            CLOSE=candle[2],
            HIGH=candle[3],
            LOW=candle[4],
            VOLUME=candle[5],
        )
