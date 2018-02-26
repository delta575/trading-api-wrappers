import pytz
from datetime import datetime
# from datetime import datetime
# from hashlib import md5

from ..base import StandardClient
from .client_auth import BitstampAuth

UTC_TIMEZONE = pytz.timezone('utc')

class BitstampStandard(StandardClient):
    def __init__(self, key=False, secret=False, customer_id=None, timeout=30):
        StandardClient.__init__(self)
        self.client = BitstampAuth(
            key=str(key), secret=str(secret), customer_id=customer_id, timeout=timeout
        )

    @staticmethod
    def name():
        return "Bitstamp"

    @staticmethod
    def get_pair_mapping(base, quote):
        return "%s%s" % (base.lower(), quote.lower())

    @staticmethod
    def get_currency_mapping(currency):
        return currency.lower()

    def get_balance(self, currency):
        return float(self.client.balance()['%s_balance' % currency])

    def get_withdrawals(self, currency):
        withdrawals = self.client.withdrawal_requests()
        types = {
            0: "sepa",
            1: "btc",
            2: "usd",
            14: "xrp",
            15: "ltc",
            16: "eth"
        }

        status = {
            0: "open",
            1: "in process",
            2: "finished",
            3: "canceled",
            4: "failed"
        }


        return [
            (
                "bitstamp-w-%s" % wdraw.get('id'),
                datetime.strptime(
                    wdraw.get('datetime'), '%Y-%m-%d %H:%M:%S'
                ).replace(tzinfo=UTC_TIMEZONE).isoformat().split(".")[0],
                "bitstamp",
                wdraw.get('id'),
                status.get(wdraw.get('status')),
                currency,
                wdraw.get('amount'),
                wdraw.get('address'),
                wdraw.get('transaction_id'),
                ''
            )
            for wdraw in withdrawals
            if types.get(wdraw.get('type')) == currency
        ]

    # def get_deposits(self, currency):
    #     deposits = self.client.deposits(
    #         currency=self.get_currency_mapping(currency)
    #     )
    #     return [
    #         (
    #             "surbtc-d-%s" % dep.id,
    #             dep.created_at.replace(tzinfo=UTC_TIMEZONE).isoformat().split(".")[0],
    #             "surbtc",
    #             dep.id,
    #             dep.state,
    #             currency,
    #             dep.amo   unt.amount,
    #             dep.data.address,
    #             dep.data.tx_hash,
    #             dep.fee.amount
    #         )
    #         for dep in deposits
    #     ]

    def get_orders(self, base, quote, state=None):
        market_id = self.get_pair_mapping(base, quote)
        params = {'limit': 1000}
        url, path = self.client.url_path_for('v2/user_transactions/%s/' % market_id)
        orders = self.client._sign_and_post(url, path, params)

        for order in orders:
            if order.get('type') != '2':   # market trade
                continue
            yield (
                "bitstamp-o-%s-%s" % (market_id, order.get('order_id')),
                datetime.strptime(
                    order.get('datetime'), '%Y-%m-%d %H:%M:%S'
                ).replace(tzinfo=UTC_TIMEZONE).isoformat().split(".")[0],
                "bitstamp",
                '',
                order.get('order_id'),
                base,
                quote,
                'Bid',
                'market',
                None,
                None,
                'traded',
                base,
                abs(float(order.get(base))),
                base,
                abs(float(order.get(base))),
                quote,
                abs(float(order.get(quote))),
                quote,
                abs(float(order.get('fee'))),
                base,
                abs(float(order.get(base))),
            )

    def get_ticker(self, base, quote, bid_ask='bid'):
        return float(self.client.ticker(
                self.get_pair_mapping(base, quote)
        )[bid_ask])


    # def get_trades(self, base, quote, timestamp=None):
    #     market_id = self.get_pair_mapping(base, quote)
    #     params = {}
    #     if timestamp is not None:
    #         params['timestamp'] = timestamp

    #     url, path = self.client.url_path_for(constants.Path.TRADES, path_arg=market_id)
    #     data = self.client.get(url, params=params)

    #     for trade in data['trades']['entries']:
    #         timestamp_ = (1.0*int(trade[0]))/1000
    #         date_iso = datetime.utcfromtimestamp(timestamp_).isoformat()
    #         trade_id = md5((",".join([str(x) for x in trade])).encode('utf-8')).hexdigest()[:9]
    #         yield (
    #             "surbtc-t-%s-%s" % (market_id, trade_id),
    #             trade_id,
    #             market_id,
    #             date_iso,
    #             "surbtc",
    #             base,
    #             float(trade[1]),
    #             quote,
    #             float(trade[2]),
    #             trade[3]
    #         )
