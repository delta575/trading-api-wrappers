import base64
import hashlib
import hmac
import json

# local
from . import constants_v1 as _c
from ..common import check_keys, clean_parameters, gen_nonce, update_dictionary
from .client_public_v1 import BitfinexPublic

_p = _c.Path


class BitfinexAuth(BitfinexPublic):

    def __init__(self, key=False, secret=False, timeout=30):
        BitfinexPublic.__init__(self, timeout)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    # INFO --------------------------------------------------------------------
    # Return information about your account (trading fees).
    def account_info(self):
        url, path = self.url_path_for(_p.ACCOUNT_INFO)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_get(url, payload)

    # Return information about your account (trading fees).
    def summary(self):
        url, path = self.url_path_for(_p.SUMMARY)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_get(url, payload)

    # Check the permissions of the key being used to generate this request.
    def key_info(self):
        url, path = self.url_path_for(_p.KEY_INFO)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_get(url, payload)

    # See your trading wallet information for margin trading.
    def margin_info(self):
        url, path = self.url_path_for(_p.MARGIN_INFO)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_get(url, payload)

    # See your balances.
    def balances(self):
        url, path = self.url_path_for(_p.BALANCES)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_get(url, payload)

    # MOVEMENTS ---------------------------------------------------------------
    # Return your deposit address to make a new deposit.
    def new_deposit(self,
                    method,
                    wallet_name,
                    renew=0):
        url, path = self.url_path_for(_p.DEPOSIT_NEW)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'method': method,
            'wallet_name': wallet_name,
            'renew': renew,
        }
        return self._sign_and_post(url, payload)

    # Allow you to move available balances between your wallets.
    def transfer(self,
                 amount,
                 currency: _c.Currency,
                 wallet_from,
                 wallet_to):
        currency = _c.Currency.check(currency).value
        url, path = self.url_path_for(_p.TRANSFER)
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
    def withdraw(self,
                 w_type,
                 wallet,
                 amount,
                 address):
        url, path = self.url_path_for(_p.WITHDRAW)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'withdraw_type': w_type,
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
                    symbol: _c.Symbol = _c.Symbol.BTCUSD,
                    params=None):
        symbol = _c.Symbol.check(symbol).value
        url, path = self.url_path_for(_p.ORDER_NEW)
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
        url, path = self.url_path_for(_p.ORDER_CANCEL)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'order_id': order_id,
        }
        return self._sign_and_post(url, payload)

    # Cancel all orders.
    def delete_all_order(self):
        url, path = self.url_path_for(_p.ORDER_CANCEL_ALL)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_post(url, payload)

    # Get the status of an order. Is it active? Was it cancelled?
    # To what extent has it been executed? etc.
    def status_order(self, order_id):
        url, path = self.url_path_for(_p.ORDER_STATUS)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'order_id': order_id,
        }
        return self._sign_and_post(url, payload)

    # View your active orders.
    def active_orders(self):
        url, path = self.url_path_for(_p.ORDERS)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_post(url, payload)

    # POSITIONS ---------------------------------------------------------------

    # View your active positions.
    def active_positions(self):
        url, path = self.url_path_for(_p.POSITIONS)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
        }
        return self._sign_and_post(url, payload)

    # Claim a position.
    def claim_position(self, position_id):
        url, path = self.url_path_for(_p.POSITION_CLAIM)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'position_id': position_id,
        }
        return self._sign_and_post(url, payload)

    # HISTORICAL DATA ---------------------------------------------------------
    # View your past deposits/withdrawals.
    def balance_history(self,
                        currency: _c.Currency,
                        since=None,
                        until=None,
                        limit=None,
                        wallet=None):
        currency = _c.Currency.check(currency).value
        url, path = self.url_path_for(_p.HISTORY)
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
                  currency: _c.Currency,
                  method=None,
                  since=None,
                  until=None,
                  limit=None):
        currency = _c.Currency.check(currency).value
        url, path = self.url_path_for(_p.HISTORY_MOVEMENTS)
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
                    symbol: _c.Symbol,
                    timestamp,
                    until=None,
                    limit_trades=None,
                    reverse=None):
        symbol = _c.Symbol.check(symbol).value
        url, path = self.url_path_for(_p.PAST_TRADES)
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
    def place_offer(self,
                    currency: _c.Currency,
                    amount,
                    rate,
                    period,
                    direction):
        currency = _c.Currency.check(currency).value
        url, path = self.url_path_for(_p.OFFER_NEW)
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
        url, path = self.url_path_for(_p.OFFER_CANCEL)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'offer_id': offer_id,
        }
        return self._sign_and_post(url, payload)

    # Get the status of an offer. Is it active? Was it cancelled?
    # To what extent has it been executed? etc.
    def status_offer(self, offer_id):
        url, path = self.url_path_for(_p.OFFER_STATUS)
        payload = {
            'request': path,
            'nonce': gen_nonce(),
            'offer_id': offer_id,
        }
        return self._sign_and_post(url, payload)

    # View your active offers.
    def active_offers(self):
        url, path = self.url_path_for(_p.OFFERS)
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
