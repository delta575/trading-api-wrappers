from ..base import Client


class BitfinexPublic(Client):
    base_url = "https://api.bitfinex.com/v1/"
    error_keys = ["message"]

    def ticker(self, symbol: str):
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
        return self.get(f"pubticker/{symbol}")

    def stats(self, symbol: str):
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
        return self.get(f"stats/{symbol}")

    def today(self, symbol: str):
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
        return self.get(f"today/{symbol}")

    def lend_book(self, currency: str, limit_bids: int = None, limit_asks: int = None):
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
        return self.get(
            f"lendbook/{currency}",
            params={
                "limit_bids": limit_bids,
                "limit_asks": limit_asks,
            },
        )

    def order_book(
        self,
        symbol: str,
        limit_bids: int = None,
        limit_asks: int = None,
        group: int = None,
    ):
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
        return self.get(
            f"book/{symbol}",
            params={
                "limit_bids": limit_bids,
                "limit_asks": limit_asks,
                "group": group,
            },
        )

    def trades(self, symbol: str, timestamp: float = None, limit_trades: int = None):
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
        return self.get(
            f"trades/{symbol}",
            params={
                "timestamp": timestamp,
                "limit_trades": limit_trades,
            },
        )

    def lends(self, currency: str, timestamp: float = None, limit_lends: int = None):
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
        return self.get(
            f"lends/{currency}",
            params={
                "timestamp": timestamp,
                "limit_lends": limit_lends,
            },
        )

    def symbols(self):
        """Get a list of valid symbol IDs.

        GET https://api.bitfinex.com/v1/symbols

        Returns:
            list: A list of symbol names as str.

        """
        return self.get("symbols")

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
        return self.get("symbols_details")
