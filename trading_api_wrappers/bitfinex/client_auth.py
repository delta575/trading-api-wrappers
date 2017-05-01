import base64
import hashlib
import hmac
import json

# local
from ..common import check_keys, clean_parameters, gen_nonce, update_dictionary
from .client_public import BitfinexPublic

# API Paths
# Info
PATH_ACCOUNT_INFO = 'account_infos'
PATH_SUMMARY = 'summary'
PATH_KEY_INFO = 'key_info'
PATH_MARGIN_INFO = 'margin_infos'
PATH_BALANCES = 'balances'
# Movements
PATH_DEPOSIT_NEW = 'deposit/new'
PATH_TRANSFER = 'transfer'
PATH_WITHDRAW = 'withdraw'
# Orders
PATH_ORDER_NEW = 'order/new'
PATH_ORDER_CANCEL = 'order/cancel'
PATH_ORDER_CANCEL_ALL = 'order/cancel/all'
PATH_ORDER_STATUS = 'order/status'
PATH_ORDERS = 'orders'
# Positions
PATH_POSITIONS = 'positions'
PATH_POSITION_CLAIM = 'position/claim'
# Historical Data
PATH_HISTORY = 'history'
PATH_HISTORY_MOVEMENTS = 'history/movements'
PATH_PAST_TRADES = 'mytrades'
# Margin Funding
PATH_OFFER_NEW = 'offer/new'
PATH_OFFER_CANCEL = 'offer/cancel'
PATH_OFFER_STATUS = 'offer/status'
PATH_OFFERS = 'offers'


class BitfinexAuth(BitfinexPublic):

    def __init__(self, key=False, secret=False, timeout=30):
        BitfinexPublic.__init__(self, timeout)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    # INFO --------------------------------------------------------------------
    # Return information about your account (trading fees).
    def account_info(self):
        url, path = self.url_path_for(PATH_ACCOUNT_INFO)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_get(url, payload)

    # Return information about your account (trading fees).
    def summary(self):
        url, path = self.url_path_for(PATH_SUMMARY)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_get(url, payload)

    # Check the permissions of the key being used to generate this request.
    def key_info(self):
        url, path = self.url_path_for(PATH_KEY_INFO)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_get(url, payload)

    # See your trading wallet information for margin trading.
    def margin_info(self):
        url, path = self.url_path_for(PATH_MARGIN_INFO)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_get(url, payload)

    # See your balances.
    def balances(self):
        url, path = self.url_path_for(PATH_BALANCES)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_get(url, payload)

    # MOVEMENTS ---------------------------------------------------------------
    # Return your deposit address to make a new deposit.
    def new_deposit(self, method, wallet_name, renew=0):
        url, path = self.url_path_for(PATH_DEPOSIT_NEW)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'method': method,
            'wallet_name': wallet_name,
            'renew': renew,
        }
        return self._sign_and_post(url, payload)

    # Allow you to move available balances between your wallets.
    def transfer(self, amount, currency, wallet_from, wallet_to):
        url, path = self.url_path_for(PATH_TRANSFER)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'amount': str(amount),
            'currency': currency,
            'walletfrom': wallet_from,
            'walletto': wallet_to,
        }
        return self._sign_and_post(url, payload)

    # Allow you to request a withdrawal from one of your wallet.
    def withdraw(self, currency, wallet, amount, address):
        url, path = self.url_path_for(PATH_WITHDRAW)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'withdraw_type': currency,
            'walletselected': wallet,
            'amount': str(amount),
            'address': address,
        }
        return self._sign_and_post(url, payload)

    # ORDERS ------------------------------------------------------------------
    # Submit a new order.
    def place_order(self,
                    amount,
                    price,
                    side,
                    ord_type,
                    symbol='btcusd',
                    params=None):
        url, path = self.url_path_for(PATH_ORDER_NEW)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'symbol': symbol,
            'amount': str(amount),
            'price': str(price),
            'side': side,
            'type': ord_type,
            'ocoorder': False,
            'buy_price_oco': 1,
            'sell_price_oco': 9999
        }
        update_dictionary(payload, params)
        return self._sign_and_post(url, payload)

    # Cancel an order.
    def delete_order(self, order_id):
        url, path = self.url_path_for(PATH_ORDER_CANCEL)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'order_id': order_id,
        }
        return self._sign_and_post(url, payload)

    # Cancel all orders.
    def delete_all_order(self):
        url, path = self.url_path_for(PATH_ORDER_CANCEL_ALL)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_post(url, payload)

    # Get the status of an order. Is it active? Was it cancelled?
    # To what extent has it been executed? etc.
    def status_order(self, order_id):
        url, path = self.url_path_for(PATH_ORDER_STATUS)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'order_id': order_id,
        }
        return self._sign_and_post(url, payload)

    # View your active orders.
    def active_orders(self):
        url, path = self.url_path_for(PATH_ORDERS)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_post(url, payload)

    # POSITIONS ---------------------------------------------------------------

    # View your active positions.
    def active_positions(self):
        url, path = self.url_path_for(PATH_POSITIONS)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_post(url, payload)

    # Claim a position.
    def claim_position(self, position_id):
        url, path = self.url_path_for(PATH_POSITION_CLAIM)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'position_id': position_id,
        }
        return self._sign_and_post(url, payload)

    # HISTORICAL DATA ---------------------------------------------------------
    # View your past deposits/withdrawals.
    def balance_history(self,
                        currency,
                        since=None,
                        until=None,
                        limit=None,
                        wallet=None):
        url, path = self.url_path_for(PATH_HISTORY)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'currency': currency,
            'since': since,
            'until': until,
            'limit': limit,
            'wallet': wallet,
        }
        return self._sign_and_post(url, payload)

    # View your past deposits/withdrawals.
    def movements(self,
                  currency,
                  method=None,
                  since=None,
                  until=None,
                  limit=None):
        url, path = self.url_path_for(PATH_HISTORY_MOVEMENTS)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'currency': currency,
            'method': method,
            'since': since,
            'until': until,
            'limit': limit,
        }
        return self._sign_and_post(url, payload)

    # View your past trades.
    def past_trades(self,
                    symbol,
                    timestamp,
                    until=None,
                    limit_trades=None,
                    reverse=None):
        url, path = self.url_path_for(PATH_PAST_TRADES)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'symbol': symbol,
            'timestamp': str(timestamp),
            'until': until,
            'limit_trades': limit_trades,
            'reverse': reverse,
        }
        return self._sign_and_post(url, payload)

    # MARGIN FUNDING ----------------------------------------------------------
    # Submit a new Offer.
    def place_offer(self, currency, amount, rate, period, direction):
        url, path = self.url_path_for(PATH_OFFER_NEW)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'currency': currency,
            'amount': amount,
            'rate': rate,
            'period': period,
            'direction': direction,
        }
        return self._sign_and_post(url, payload)

    # Cancel an offer.
    def cancel_offer(self, offer_id):
        url, path = self.url_path_for(PATH_OFFER_CANCEL)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'offer_id': offer_id,
        }
        return self._sign_and_post(url, payload)

    # Get the status of an offer. Is it active? Was it cancelled?
    # To what extent has it been executed? etc.
    def status_offer(self, offer_id):
        url, path = self.url_path_for(PATH_OFFER_STATUS)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'offer_id': offer_id,
        }
        return self._sign_and_post(url, payload)

    # View your active offers.
    def active_offers(self):
        url, path = self.url_path_for(PATH_OFFERS)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_post(url, payload)

    # PRIVATE METHODS ---------------------------------------------------------
    # Pack and sign the payload of the request.
    def _sign_payload(self, payload):

        j = json.dumps(payload).encode('utf-8')
        encoded_body = base64.standard_b64encode(j)

        h = hmac.new(self.SECRET.encode('utf-8'), encoded_body, hashlib.sha384)
        signature = h.hexdigest()

        return {
            'X-BFX-APIKEY': self.KEY,
            'X-BFX-SIGNATURE': signature,
            'X-BFX-PAYLOAD': encoded_body,
        }

    # Packs and sign the payload and send the request with GET.
    def _sign_and_get(self, url, payload):
        payload = clean_parameters(payload)
        signed_payload = self._sign_payload(payload)
        return self.get(url, headers=signed_payload)

    # Packs and sign the payload and send the request with POST.
    def _sign_and_post(self, url, payload):
        payload = clean_parameters(payload)
        signed_payload = self._sign_payload(payload)
        return self.post(url, headers=signed_payload, data=payload)
