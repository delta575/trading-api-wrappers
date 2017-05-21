# local
from . import constants_v1 as _c
from ..base import Client
from .server import BitfinexServerV1 as Server

_p = _c.Path


class BitfinexPublic(Client):

    def __init__(self, timeout=30):
        Client.__init__(self, Server(), timeout)

    def ticker(self, symbol: _c.Symbol=_c.Symbol.BTCUSD):
        """Gets the innermost bid and asks and information on the most recent trade.

        The ticker is a high level overview of the state of the market. It
        shows you the current best bid and ask, as well as the last trade
        price. It also includes information such as daily volume and how much
        the price has moved over the last day.

        GET https://api.bitfinex.com/v1/pubticker/[symbol]

        Args:
            symbol (str): (Required)
                The symbol you want information about.
                You can find the list of valid symbols by calling the /symbols
                endpoint.

        Returns:
            dict: A dictionary of the following:

            Key         Type                Description
            mid         [float as str]      (bid + ask) / 2
            bid         [float as str]      Innermost bid
            ask         [float as str]      Innermost ask
            last_price  [float as str]      The price at which the last order
                                            executed
            low         [float as str]      Lowest trade price of the last 24h
            high        [float as str]      Highest trade price of the last 24h
            volume      [float as str]      Trading volume of the last 24h
            timestamp   [float as str]      The timestamp at which this
                                            information was valid

        """
        symbol = _c.Symbol.check(symbol).value
        url = self.url_for(_p.TICKER, path_arg=symbol)
        return self.get(url)

    def stats(self, symbol: _c.Symbol):
        """Various statistics about the requested pair.

        GET https://api.bitfinex.com/v1/stats/[symbol]

        Args:
            symbol (str): (Required)
                The symbol you want information about.
                You can find the list of valid symbols by calling the /symbols
                endpoint.

        Returns:
            list: A list of dicts with the following:

            Key     Type                Description
            period  [int]               Period covered in days
            volume  [float as str]      Volume in the period

        """
        symbol = _c.Symbol.check(symbol).value
        url = self.url_for(_p.STATS, path_arg=symbol)
        return self.get(url)

    def today(self, symbol: _c.Symbol):
        """Today's low, high and volume.

        GET https://api.bitfinex.com/v1/today/[symbol]

        Args:
            symbol (str): (Required)
                The symbol you want information about.
                You can find the list of valid symbols by calling the /symbols
                endpoint.

        Returns:
            dict: A dictionary of the following:

            Key     Type                Description
            volume  [float as str]      Today's volume
            high    [float as str]      Today's high price
            low     [float as str]      Today's low price

        """
        symbol = _c.Symbol.check(symbol).value
        url = self.url_for(_p.TODAY, path_arg=symbol)
        return self.get(url)

    def lend_book(self,
                  currency: _c.Currency,
                  limit_bids=None,
                  limit_asks=None):
        """Get the full margin funding book.

        GET https://api.bitfinex.com/v1/lendbook/[currency]

        Args:
            currency (str): (Required)
                Currency (USD, BTC, etc.)

            limit_bids (int): (Optional, default=50)
                Limit the number of bids returned. May be 0 in which case the
                array of bids is empty.

            limit_asks (int): (Optional, default=50)
                Limit the number of asks returned. May be 0 in which case the
                array of bids is empty.

        Returns:
            dict: A dictionary of the following:

            Key     Type                Description
            bids    [list of dicts]     Array of funding bids
            asks    [list of dicts]     Array of funding asks

            Detail of each dict:

            Key	        Type            Description
            rate        [float as str]  Rate in % per 365 days
            amount      [float as str]
            period      [int]           Minimum period for the margin funding
                                        contract in days
            timestamp   [float as str]
            frr	        [str]           “Yes” if the offer is at Flash Return
                                        Rate, “No” if the offer is at fixed
                                        rate

        """
        currency = _c.Currency.check(currency).value
        parameters = {
            'limit_bids': limit_bids,
            'limit_asks': limit_asks,
        }
        url = self.url_for(_p.LEND_BOOK, path_arg=currency)
        return self.get(url, params=parameters)

    def order_book(self,
                   symbol: _c.Symbol,
                   limit_bids=None,
                   limit_asks=None,
                   group=None):
        """Get the full order book.

        GET https://api.bitfinex.com/v1/book/[symbol]

        Args:
            symbol (str): (Required)
                The symbol you want information about.
                You can find the list of valid symbols by calling the /symbols
                endpoint.

            limit_bids (int): (Optional, default=50)
                Limit the number of bids returned. May be 0 in which case the
                array of bids is empty.

            limit_asks (int): (Optional, default=50)
                Limit the number of asks returned. May be 0 in which case the
                array of bids is empty.

            group (int): (Optional, default=1)
                If 1, orders are grouped by price in the order book. If 0,
                orders are sorted individually.

        Returns:
            dict: A dictionary of the following:

            Key     Type                Description
            bids    [list of dicts]     Array of bid orders
            asks    [list of dicts]     Array of ask orders

            Detail of each dict:

            Key         Type            Description
            price       [float as str]
            amount      [float as str]
            timestamp   [float as str]

        """
        symbol = _c.Symbol.check(symbol).value
        parameters = {
            'limit_bids': limit_bids,
            'limit_asks': limit_asks,
            'group': group,
        }
        url = self.url_for(_p.ORDER_BOOK, path_arg=symbol)
        return self.get(url, params=parameters)

    def trades(self,
               symbol: _c.Symbol,
               timestamp=None,
               limit_trades=None):
        """Get a list of the most recent trades for the given symbol.

        GET https://api.bitfinex.com/v1/trades/[symbol]

        Args:
            symbol (str): (Required)
                The symbol you want information about.
                You can find the list of valid symbols by calling the /symbols
                endpoint.

            timestamp (float): (Optional)
                Only show trades at or after this timestamp.

            limit_trades (int): (Optional, default=50)
                Limit the number of trades returned. Must be >= 1.

        Returns:
            list: A list of dicts with the following:

            Key         Type            Description
            tid         [int]
            timestamp   [int]
            price       [float as str]
            amount      [float as str]
            exchange    [str]
            type        [str]           'sell' or 'buy'
                                        (can be '' if undetermined)

        """
        symbol = _c.Symbol.check(symbol).value
        parameters = {
            'timestamp': timestamp,
            'limit_trades': limit_trades,
        }
        url = self.url_for(_p.TRADES, path_arg=symbol)
        return self.get(url, params=parameters)

    def lends(self,
              currency: _c.Currency,
              timestamp=None,
              limit_lends=None):
        """Get a list of the most recent lending data for the given currency:

        Total amount lent and rate (in % by 365 days).

        GET https://api.bitfinex.com/v1/lends/[currency]

        Args:
            currency (str): (Required)
                Currency (USD, BTC, etc.)

            timestamp (float): (Optional)
                Only show data at or after this timestamp.

            limit_lends (int): (Optional, default=50)
                Limit the amount of funding data returned. Must be >= 1.

        Returns:
            list: A list of dicts with the following:

            Key         Type	        Description
            rate        [float as str]	Average rate of total funding received
                                        at fixed rates, ie past Flash Return
                                        Rate annualized (% by 365 days)
            amount_lent [float as str]  Total amount of open margin funding in
                                        the given currency
            amount_used [float as str]  Total amount of open margin funding
                                        used in a margin position
                                        in the given currency
            timestamp   [int]

        """
        currency = _c.Currency.check(currency).value
        parameters = {
            'timestamp': timestamp,
            'limit_lends': limit_lends,
        }
        url = self.url_for(_p.LENDS, path_arg=currency)
        return self.get(url, params=parameters)

    def symbols(self):
        """Get a list of valid symbol IDs.

        GET https://api.bitfinex.com/v1/symbols

        Returns:
            list: A list of symbol names as str.

        """
        url = self.url_for(_p.SYMBOLS)
        return self.get(url)

    def symbols_details(self):
        """Get a list of valid symbol IDs and the pair details.

        GET https://api.bitfinex.com/v1/symbols_details

        Returns:
            list: A list of dicts with the following:

            Key                 Type            Description
            pair                [str]           The pair code (symbol)
            price_precision     [int]           Maximum number of significant
                                                digits for price in this pair
            initial_margin      [float as str]  Initial margin required to open
                                                a position in this pair
            minimum_margin      [float as str]  Minimal margin to maintain (%)
            maximum_order_size  [float as str]  Maximum order size of the pair
            expiration          [str]           Expiration date for limited
                                                contracts/pairs

        """
        url = self.url_for(_p.SYMBOLS_DETAILS)
        return self.get(url)
