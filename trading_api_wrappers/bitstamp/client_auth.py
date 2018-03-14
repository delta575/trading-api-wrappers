import hashlib
import hmac

# local
from .client_public import BitstampPublic
from ..common import check_keys, clean_parameters, gen_nonce


class BitstampAuth(BitstampPublic):

    def __init__(self, key, secret, customer_id, timeout=30):
        super().__init__(timeout)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)
        self.CUSTOMER_ID = str(customer_id)

    # Private user data -------------------------------------------------------
    def account_balance(self, currency_pair: str=None):
        """
        Returns amounts available and reserved per currency,
        also fee percentage for the currency pair, or for all currency pairs
        if no pair was specified:

            {'btc_reserved': '0',
             'fee': '0.5000',
             'btc_available': '2.30856098',
             'usd_reserved': '0',
             'btc_balance': '2.30856098',
             'usd_balance': '114.64',
             'usd_available': '114.64',
             ...
             ---If currency pair was specified:
             'fee': '',
             ---If currency pair was not specified:
             'btcusd_fee': '0.25',
             'btceur_fee': '0.25',
             'eurusd_fee': '0.20',
             ...
             }
        """
        path = f'balance/{currency_pair}' if currency_pair else 'balance'
        url = self.url_for(path)
        return self._sign_and_post(url)

    def user_transactions(self,
                          currency_pair: str=None,
                          offset: int=None,
                          limit: int=None,
                          sort_desc: bool=None):
        """
        Returns descending list of transactions. Every transaction (dictionary)
        contains:
        
            {'usd': '-39.25',
             'datetime': '2013-03-26 18:49:13',
             'fee': '0.20',
             'btc': '0.50000000',
             'type': 2,
             'id': 213642}
             
        Instead of the keys btc and usd, it can contain other currency codes
        """
        payload = {
            'offset': offset,
            'limit': limit,
        }
        if sort_desc is not None:
            payload['sort'] = 'desc' if sort_desc else 'asc'
        path = 'user_transactions'
        path = path if currency_pair else f'{path}/{currency_pair}'
        url = self.url_for(path)
        return self._sign_and_post(url, payload)

    # Orders ------------------------------------------------------------------
    def open_orders(self, currency_pair: str=None):
        """
        Returns JSON list of open orders. Each order is represented as a
        dictionary.
        """
        path = f"open_orders/{currency_pair or 'all'}"
        url = self.url_for(path)
        return self._sign_and_post(url)

    def orders_status(self, order_id: int):
        """
        Returns dictionary.
        - status: 'Finished'
          or      'In Queue'
          or      'Open'
        - transactions: list of transactions
          Each transaction is a dictionary with the following keys:
              btc, usd, price, type, fee, datetime, tid
          or  btc, eur, ....
          or  eur, usd, ....
        """
        payload = {'id': order_id}
        url = self.url_for('order_status', version=1)
        return self._sign_and_post(url, payload)

    def cancel_order(self, order_id: int):
        """
        Cancel the order specified by order_id.

        Returns dictionary of the canceled order, containing the keys:
        id, type, price, amount
        """
        payload = {'id': order_id}
        url = self.url_for('cancel_order')
        return self._sign_and_post(url, payload)

    def cancel_all_orders(self):
        """
        Cancel all open orders.

        Returns True if it was successful
        """
        url = self.url_for('cancel_all_orders', version=1)
        return self._sign_and_post(url)

    def _limit_order(self,
                     path,
                     currency_pair: str,
                     amount: float,
                     price: float,
                     limit_price: float=None,
                     daily_order: bool=None):
        payload = {
            'amount': amount,
            'price': price,
            'limit_price': limit_price,
            'daily_order': daily_order,
        }
        url = self.url_for(path, currency_pair)
        return self._sign_and_post(url, payload)

    def _market_order(self,
                      path: str,
                      currency_pair: str,
                      amount: float):
        payload = {'amount': amount}
        url = self.url_for(path, currency_pair)
        return self._sign_and_post(url, payload)

    def buy_limit_order(self,
                        currency_pair: str,
                        amount: float,
                        price: float,
                        limit_price: float,
                        daily_order: bool=None):
        """
        Order to buy amount for specified price.
        """
        return self._limit_order('buy/%s', currency_pair, amount,
                                 price, limit_price, daily_order)

    def sell_limit_order(self,
                         currency_pair: str,
                         amount: float,
                         price: float,
                         limit_price: float,
                         daily_order: bool=None):
        """
        Order to sell amount for specified price.
        """
        return self._limit_order('sell/%s', currency_pair, amount,
                                 price, limit_price, daily_order)

    def buy_market_order(self,
                         currency_pair: str,
                         amount: float):
        """
        Order to buy amount for market price.
        """
        return self._market_order('buy/market/%s', currency_pair, amount)

    def sell_market_order(self,
                          currency_pair: str,
                          amount: float):
        """
        Order to sell amount for market price.
        """
        return self._market_order('sell/market/%s', currency_pair, amount)

    # Withdrawals -------------------------------------------------------------
    def withdrawal_requests(self, time_delta: int=None):
        """
        Returns list of withdrawal requests.

        Each request is represented as a dictionary.

        By default, the last 24 hours (86400 seconds) are returned.
        """
        payload = {'timedelta': time_delta}
        url = self.url_for('withdrawal-requests')
        return self._sign_and_post(url, payload)

    def withdrawal(self,
                   method: str,
                   address: str,
                   amount: float,
                   version: int=2,
                   **kwargs):
        payload = {
            'amount': amount,
            'address': address,
            **kwargs
        }
        url = self.url_for(f'{method}_withdrawal', version=version)
        return self._sign_and_post(url, payload)

    def bitcoin_withdrawal(self, address: str, amount: float,
                           instant: bool=None):
        """
        Send bitcoin to another bitcoin wallet specified by address.
        """
        kwargs = {
            'version': 1,
            'instant': (1 if instant else 0) if instant else None,
        }
        return self.withdrawal('bitcoin', address, amount, **kwargs)

    def ripple_withdrawal(self, address: str, amount: float, currency: str):
        """
        Returns true if successful.
        """
        return self.withdrawal('ripple', address, amount,
                               version=1, currency=currency)

    def litecoin_withdrawal(self, address: str, amount: float):
        """
        Send litecoin to another litecoin wallet specified by address.
        """
        return self.withdrawal('ltc', address, amount)

    def eth_withdrawal(self, address: str, amount: float):
        """
        Send ether to another ether wallet specified by address.
        """
        return self.withdrawal('eth', address, amount)

    def bch_withdrawal(self, address: str, amount: float):
        """
        Send bitcoin cash to another bitcoin cash wallet specified by address.
        """
        return self.withdrawal('bch', address, amount)

    def xrp_withdrawal(self, address: str, amount: float,
                       destination_tag: str=None):
        """
        Sends xrp to another xrp wallet specified by address.
        Returns withdrawal id.
        """
        return self.withdrawal('xrp', address, amount,
                               destination_tag=destination_tag)

    # Deposits ----------------------------------------------------------------
    def deposit_address(self,
                        method: str,
                        version: int=2):
        url = self.url_for('%s_address' % method, version=version)
        return self._sign_and_post(url)

    def bitcoin_deposit_address(self):
        """
        Returns bitcoin deposit address as unicode string
        """
        return self.deposit_address('bitcoin_deposit', version=1)

    def ripple_deposit_address(self):
        """
        Returns ripple deposit address as unicode string.
        """
        return self.deposit_address('ripple', version=1)

    def litecoin_deposit_address(self):
        """
        Returns litecoin deposit address as unicode string
        """
        return self.deposit_address('ltc')

    def eth_deposit_address(self):
        """
        Returns ethereum deposit address as unicode string
        """
        return self.deposit_address('eth')

    def bch_deposit_address(self):
        """
        Returns bitcoin cash deposit address as unicode string
        """
        return self.deposit_address('bch')

    def xrp_deposit_address(self):
        """
        Returns ripple deposit address and destination tag as dictionary.
        Example:
            {'destination_tag': 53965834,
             'address': 'rDsBeAmAa4FFwbQTJp9Rs84Q56vCiWCaBx'}
        """
        return self.deposit_address('xrp')

    def unconfirmed_bitcoin_deposits(self):
        """
        Returns JSON list of unconfirmed bitcoin transactions.
        Each transaction is represented as dictionary:

        amount
          bitcoin amount
        address
          deposit address used
        confirmations
          number of confirmations
        """
        url = self.url_for('unconfirmed_btc', version=1)
        return self._sign_and_post(url)

    # Transfers ---------------------------------------------------------------
    def _transfer(self,
                  path: str,
                  amount: float,
                  currency: str,
                  sub_account: int=None):
        payload = {
            'amount': amount,
            'currency': currency,
            'subAccount': sub_account,
        }
        url = self.url_for(path)
        return self._sign_and_post(url, payload)

    def transfer_to_main(self,
                         amount: float,
                         currency: str,
                         sub_account: int=None):
        """
        Returns dictionary with status.
        sub account has to be the numerical id of the sub account, not the name
        """
        return self._transfer(
            'transfer-to-main', amount, currency, sub_account)

    def transfer_from_main(self,
                           amount: float,
                           currency: str,
                           sub_account: int):
        """
        Returns dictionary with status.
        sub account has to be the numerical id of the sub account, not the name
        """
        return self._transfer(
            'transfer-from-main', amount, currency, sub_account)

    # TODO: Bank methods

    # PRIVATE METHODS ---------------------------------------------------------
    def _sign_payload(self, payload=None):
        payload = payload or {}
        payload['key'] = self.KEY
        payload['nonce'] = gen_nonce()
        msg = str(payload['nonce']) + self.CUSTOMER_ID + self.KEY
        payload['signature'] = hmac.new(
            self.SECRET.encode('utf-8'),
            msg=msg.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()
        return payload

    def _encode_data(self, data):
        return data

    # Packs and sign the payload and send the request with POST.
    def _sign_and_post(self, url, payload=None):
        clean_payload = clean_parameters(payload)
        signed_payload = self._sign_payload(clean_payload)
        return self.post(url, headers=None, data=signed_payload)
