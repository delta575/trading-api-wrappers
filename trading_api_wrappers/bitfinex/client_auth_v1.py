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
        return self._sign_and_get(_p.ACCOUNT_INFO)

    # Return information about your account (trading fees).
    def summary(self):
        return self._sign_and_get(_p.SUMMARY)

    # Check the permissions of the key being used to generate this request.
    def key_info(self):
        return self._sign_and_get(_p.KEY_INFO)

    # See your trading wallet information for margin trading.
    def margin_info(self):
        return self._sign_and_get(_p.MARGIN_INFO)

    # See your balances.
    def balances(self):
        return self._sign_and_get(_p.BALANCES)

    # MOVEMENTS ---------------------------------------------------------------
    # Return your deposit address to make a new deposit.
    def new_deposit(self,
                    method,
                    wallet_name,
                    renew=0):
        payload = {
            'method': method,
            'wallet_name': wallet_name,
            'renew': renew,
        }
        return self._sign_and_post(_p.DEPOSIT_NEW, payload)

    # Allow you to move available balances between your wallets.
    def transfer(self,
                 amount,
                 currency: _c.Currency,
                 wallet_from,
                 wallet_to):
        payload = {
            'amount': str(amount),
            'currency': _c.Currency.check(currency).value,
            'walletfrom': wallet_from,
            'walletto': wallet_to,
        }
        return self._sign_and_post(_p.TRANSFER, payload)

    # Allow you to request a withdrawal from one of your wallet.
    def withdraw(self,
                 w_type,
                 wallet,
                 amount,
                 address):
        payload = {
            'withdraw_type': w_type,
            'walletselected': wallet,
            'amount': str(amount),
            'address': address,
        }
        return self._sign_and_post(_p.WITHDRAW, payload)

    # ORDERS ------------------------------------------------------------------
    # Submit a new order.
    def place_order(self,
                    amount,
                    price,
                    side,
                    ord_type,
                    symbol: _c.Symbol = _c.Symbol.BTCUSD,
                    params=None):
        payload = {
            'symbol': _c.Symbol.check(symbol).value,
            'amount': str(amount),
            'price': str(price),
            'side': side,
            'type': ord_type,
            'ocoorder': False,
            'buy_price_oco': 1,
            'sell_price_oco': 9999
        }
        update_dictionary(payload, params)
        return self._sign_and_post(_p.ORDER_NEW, payload)

    # Cancel an order.
    def delete_order(self, order_id):
        payload = {
            'order_id': order_id,
        }
        return self._sign_and_post(_p.ORDER_CANCEL, payload)

    # Cancel all orders.
    def delete_all_order(self):
        return self._sign_and_post(_p.ORDER_CANCEL_ALL)

    # Get the status of an order. Is it active? Was it cancelled?
    # To what extent has it been executed? etc.
    def status_order(self, order_id):
        payload = {
            'order_id': order_id,
        }
        return self._sign_and_post(_p.ORDER_STATUS, payload)

    # View your active orders.
    def active_orders(self):
        return self._sign_and_post(_p.ORDERS_ACTIVE)

    # View your latest inactive orders.
    # Limited to last 3 days and 1 request per minute.
    def orders_history(self, limit):
        payload = {
            'limit': limit,
        }
        return self._sign_and_post(_p.ORDER_HISTORY, payload)

    # POSITIONS ---------------------------------------------------------------
    # View your active positions.
    def active_positions(self):
        return self._sign_and_post(_p.POSITIONS)

    # Claim a position.
    def claim_position(self, position_id):
        payload = {
            'position_id': position_id,
        }
        return self._sign_and_post(_p.POSITION_CLAIM, payload)

    # HISTORICAL DATA ---------------------------------------------------------
    # View all of your balance ledger entries.
    def balance_history(self,
                        currency: _c.Currency,
                        since=None,
                        until=None,
                        limit=None,
                        wallet=None):
        payload = {
            'currency': _c.Currency.check(currency).value,
            'since': since,
            'until': until,
            'limit': limit,
            'wallet': wallet,
        }
        return self._sign_and_post(_p.HISTORY, payload)

    # View your past deposits/withdrawals.
    def movements(self,
                  currency: _c.Currency,
                  method=None,
                  since=None,
                  until=None,
                  limit=None):
        payload = {
            'currency': _c.Currency.check(currency).value,
            'method': method,
            'since': since,
            'until': until,
            'limit': limit,
        }
        return self._sign_and_post(_p.HISTORY_MOVEMENTS, payload)

    # View your past trades.
    def past_trades(self,
                    symbol: _c.Symbol,
                    timestamp=None,
                    until=None,
                    limit_trades=None,
                    reverse=None):
        payload = {
            'symbol': _c.Symbol.check(symbol).value,
            'timestamp': timestamp,
            'until': until,
            'limit_trades': limit_trades,
            'reverse': reverse,
        }
        return self._sign_and_post(_p.PAST_TRADES, payload)

    # MARGIN FUNDING ----------------------------------------------------------
    # Submit a new Offer.
    def place_offer(self,
                    currency: _c.Currency,
                    amount,
                    rate,
                    period,
                    direction):
        payload = {
            'currency': _c.Currency.check(currency).value,
            'amount': amount,
            'rate': rate,
            'period': period,
            'direction': direction,
        }
        return self._sign_and_post(_p.OFFER_NEW, payload)

    # Cancel an offer.
    def cancel_offer(self, offer_id):
        payload = {
            'offer_id': offer_id,
        }
        return self._sign_and_post(_p.OFFER_CANCEL, payload)

    # Get the status of an offer. Is it active? Was it cancelled?
    # To what extent has it been executed? etc.
    def status_offer(self, offer_id):
        payload = {
            'offer_id': offer_id,
        }
        return self._sign_and_post(_p.OFFER_STATUS, payload)

    # View your active offers.
    def active_offers(self):
        return self._sign_and_post(_p.OFFERS)

    # PRIVATE METHODS ---------------------------------------------------------
    # Pack and sign the payload of the request.
    def _sign_payload(self, path, payload):

        payload['request'] = path
        payload['nonce'] = gen_nonce()
        payload = clean_parameters(payload)

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
    def _sign_and_get(self, path, payload=None):
        url, path = self.url_path_for(path)
        signed_payload = self._sign_payload(path, payload or {})
        return self.get(url, headers=signed_payload)

    # Packs and sign the payload and send the request with POST.
    def _sign_and_post(self, path, payload=None):
        url, path = self.url_path_for(path)
        signed_payload = self._sign_payload(path, payload or {})
        return self.post(url, headers=signed_payload, data=payload)
