import krakenex

# local
from trading_api_wrappers.kraken.client_public import KrakenPublic
from trading_api_wrappers.common import clean_parameters

# API Paths
# Private user data
PATH_BALANCE = 'private/Balance'
PATH_TRADE_BALANCE = 'private/TradeBalance'
PATH_OPEN_ORDERS = 'private/OpenOrders'
PATH_CLOSED_ORDERS = 'private/ClosedOrders'
PATH_QUERY_ORDERS = 'private/QueryOrders'
PATH_TRADES_HISTORY = 'private/TradesHistory'
PATH_QUERY_TRADES = 'private/QueryTrades'
PATH_OPEN_POSITIONS = 'private/OpenPositions'
PATH_LEDGERS = 'private/Ledgers'
PATH_QUERY_LEDGERS = 'private/QueryLedgers'
PATH_TRADE_VOLUME = 'private/TradeVolume'
# Private user trading
PATH_ADD_ORDER = 'private/AddOrder'
PATH_CANCEL_ORDER = 'private/CancelOrder'
# Private user funding
PATH_DEPOSIT_METHODS = 'private/DepositMethods'
PATH_DEPOSIT_ADDRESSES = 'private/DepositAddresses'
PATH_DEPOSIT_STATUS = 'private/DepositStatus'
PATH_WITHDRAW_INFO = 'private/WithdrawInfo'
PATH_WITHDRAW = 'private/Withdraw'
PATH_WITHDRAW_STATUS = 'private/WithdrawStatus'
PATH_WITHDRAW_CANCEL = 'private/WithdrawCancel'


class KrakenAuth(KrakenPublic):

    def __init__(self, key=False, secret=False, test=False, timeout=30):
        KrakenPublic.__init__(self, timeout)
        self.KEY = str(key)
        self.SECRET = str(secret)
        self.TEST = test
        self.krakenex = krakenex.API(key=self.KEY,secret=self.SECRET)

    # Private user data  --------------------------------------------------------------------
    # Get account balance.
    def balance(self):
        return self.krakenex.query_private('Balance')

    # Get trade balance.
    def trade_balance(self, asset_class='currency', asset='ZUSD'):
        req = {
            'aclass': asset_class,
            'asset': asset,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('TradeBalance',req)

    # Get open orders.
    def open_orders(self, include_trades=False, userref=None):
        req = {
            'trades': include_trades,
            'userref': userref,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('OpenOrders',req)

    # Get closed orders.
    def closed_orders(self, include_trades=False, userref=None, start=None, end=None, ofs=None, closetime='both'):
        req = {
            'trades': include_trades,
            'userref': userref,
            'start': start,
            'end': end,
            'ofs': ofs,
            'closetime': closetime,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('ClosedOrders',req)

    # Query orders info.
    def query_orders(self, txid=None, include_trades=False, userref=None):
        req = {
            'trades': include_trades,
            'userref': userref,
            'txid': txid,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('ClosedOrders',req)

    # Get trades history.
    def trades_history(self, type='all', include_trades=False, start=None, end=None, ofs=None):
        req = {
            'type': type,
            'trades': include_trades,
            'start': start,
            'end': end,
            'ofs': ofs,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('TradesHistory',req)

    # Query trades info.
    def query_trades(self, txid, include_trades=False):
        req = {
            'txid': txid,
            'trades': include_trades,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('QueryTrades',req)

    # Query trades info.
    def open_positions(self, txid=None, include_pl=False):
        req = {
            'txid': txid,
            'docalcs': include_pl,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('OpenPositions',req)

    # Get ledgers info.
    def ledgers(self, asset_class='currency', asset='all', type='all', start=None, end=None, ofs=None):
        req = {
            'aclass': asset_class,
            'asset': asset,
            'type': type,
            'start': start,
            'end': end,
            'ofs': ofs,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('Ledgers',req)

    # Query ledgers.
    def query_ledgers(self, ledger_id):
        req = {
            'id': ledger_id,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('QueryLedgers',req)

    # Get trade volume.
    def trade_volume(self, pair=None, fee_info=None):
        req = {
            'pair': pair,
            'fee-info': fee_info,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('TradeVolume',req)

    # Private user trading  --------------------------------------------------------------------
    # Add standard order
    def add_order(self, pair, direction, order_type, price, volume, price2=None, leverage=None,
                  oflags=None, starttm=0, expiretm=0, userref=None, validate=None,
                  c_ordertype=None, c_price=None, c_price2=None):
        if self.TEST:
            validate = True
        req = {
            'pair': pair,
            'type': direction,
            'ordertype': order_type,
            'price': price,
            'price2': price2,
            'volume': volume,
            'leverage': leverage,
            'oflags': oflags,
            'starttm': starttm,
            'expiretm': expiretm,
            'userref': userref,
            'validate': validate,
            'close[ordertype]': c_ordertype,
            'close[price]': c_price,
            'close[price2]': c_price2,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('AddOrder',req)

        # Cancel open order
    def cancel_order(self, txid):
        req = {
            'txid': txid,
        }
        req = clean_parameters(req)
        return self.krakenex.query_private('AddOrder', req)

    # Private user funding  --------------------------------------------------------------------
    # Get deposit methods.
    def deposit_methods(self):
        pass

    # Get deposit addresses
    def deposit_addresses(self):
        pass

    # Get status of recent deposits
    def deposit_status(self):
        pass

    # Get withdrawal information
    def withdraw_info(self):
        pass

    # Withdraw funds
    def withdraw_funds(self):
        pass

    # Get status of recent withdrawals
    def withdraw_status(self):
        pass

    # Request withdrawal cancelation
    def withdraw_cancel(self):
        pass