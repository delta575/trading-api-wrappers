from enum import Enum


# API paths
class Path(object):
    MARKETS = 'markets'
    MARKET_DETAILS = 'markets/%s'
    TICKER = "markets/%s/ticker"
    ORDER_BOOK = 'markets/%s/order_book'
    QUOTATION = 'markets/%s/quotations'
    FEE_PERCENTAGE = 'markets/%s/fee_percentage'
    TRADE_TRANSACTIONS = 'markets/%s/trade_transactions'
    REPORTS = 'markets/%s/reports'
    BALANCES = 'balances/%s'
    BALANCES_EVENTS = 'balance_events'
    ORDERS = 'markets/%s/orders'
    SINGLE_ORDER = 'orders/%s'
    WITHDRAWAL = 'currencies/%s/withdrawals'


class Currency(Enum):
    BTC = 'BTC'
    CLP = 'CLP'
    COP = 'COP'

    @staticmethod
    def check_param(currency):
        if not isinstance(currency, Currency):
            try:
                currency = Currency[str(currency).upper()]
            except KeyError:
                msg = f"Param '{currency}' is not a valid currency!"
                raise ValueError(msg) from None
        return currency


class Market(Enum):
    BTC_CLP = 'BTC-CLP'
    BTC_COP = 'BTC-COP'

    @staticmethod
    def check_param(market_id):
        if not isinstance(market_id, Market):
            try:
                market_id = Market[str(market_id).replace('-', '_').upper()]
            except KeyError:
                msg = f"Param '{market_id}' is not a valid Market ID!"
                raise ValueError(msg) from None
        return market_id


class QuotationType(Enum):
    BID_GIVEN_SIZE = 'bid_given_size'
    BID_GIVEN_EARNED_BASE = 'bid_given_earned_base'
    BID_GIVEN_SPENT_QUOTE = 'bid_given_spent_quote'
    ASK_GIVEN_SIZE = 'ask_given_size'
    ASK_GIVEN_EARNED_QUOTE = 'ask_given_earned_quote'
    ASK_GIVEN_SPENT_BASE = 'ask_given_spent_base'

    @staticmethod
    def check_param(q_type):
        if not isinstance(q_type, QuotationType):
            try:
                q_type = QuotationType[str(q_type).upper()]
            except KeyError:
                msg = f"Param '{q_type}' is not a valid Quotation Type!"
                raise ValueError(msg) from None
        return q_type


class OrderType(Enum):
    ASK = 'Ask'
    BID = 'Bid'

    @staticmethod
    def check_param(order_type):
        if not isinstance(order_type, OrderType):
            try:
                order_type = OrderType[str(order_type).upper()]
            except KeyError:
                msg = f"Param '{order_type}' is not a valid Order Type!"
                raise ValueError(msg) from None
        return order_type


class OrderPriceType(Enum):
    MARKET = 'market'
    LIMIT = 'limit'

    @staticmethod
    def check_param(price_type):
        if not isinstance(price_type, OrderPriceType):
            try:
                price_type = OrderPriceType[str(price_type).upper()]
            except KeyError:
                msg = f"Param '{price_type}' is not a valid Price Type!"
                raise ValueError(msg) from None
        return price_type


class OrderState(Enum):
    RECEIVED = 'received'
    PENDING = 'pending'
    TRADED = 'traded'
    CANCELING = 'canceling'
    CANCELED = 'canceled'

    @staticmethod
    def check_param(state):
        if state and not isinstance(state, OrderState):
            try:
                state = OrderState[str(state).upper()]
            except KeyError:
                msg = f"Param '{state}' is not a valid Order State!"
                raise ValueError(msg) from None
        return state


class BalanceEvent(Enum):
    DEPOSIT_CONFIRM = 'deposit_confirm'
    WITHDRAWAL_CONFIRM = 'withdrawal_confirm'
    TRANSACTION = 'transaction'
    TRANSFER_CONFIRMATION = 'transfer_confirmation'

    @staticmethod
    def check_param(event_name):
        if event_name and not isinstance(event_name, BalanceEvent):
            try:
                event_name = BalanceEvent[str(event_name).upper()]
            except KeyError:
                msg = f"Param '{event_name}' is not a valid Event Name!"
                raise ValueError(msg) from None
        return event_name
