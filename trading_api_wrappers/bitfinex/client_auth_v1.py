import base64
import hashlib
import hmac
import json

# local
from .client_public_v1 import BitfinexPublic
from ..common import check_keys, clean_parameters, gen_nonce


class BitfinexAuth(BitfinexPublic):

    def __init__(self, key: str=False, secret: str=False, timeout: int=30,
                 retry=None):
        super().__init__(timeout, retry)
        check_keys(key, secret)
        self.KEY = str(key)
        self.SECRET = str(secret)

    # INFO --------------------------------------------------------------------
    # Return information about your account (trading fees).
    def account_info(self):
        return self._sign_and_get('account_infos')

    # Return information about your account (trading fees).
    def summary(self):
        return self._sign_and_get('summary')

    # Check the permissions of the key being used to generate this request.
    def key_info(self):
        return self._sign_and_get('key_info')

    # See your trading wallet information for margin trading.
    def margin_info(self):
        return self._sign_and_get('margin_infos')

    # See your balances.
    def balances(self):
        return self._sign_and_get('balances')

    # MOVEMENTS ---------------------------------------------------------------
    # Return your deposit address to make a new deposit.
    def new_deposit(self,
                    method: str,
                    wallet_name: str,
                    renew: bool=None):
        payload = {
            'method': method,
            'wallet_name': wallet_name,
            'renew': renew if renew is not None else None,
        }
        return self._sign_and_post('deposit/new', payload)

    # Allow you to move available balances between your wallets.
    def transfer(self,
                 amount: float,
                 currency: str,
                 wallet_from: str,
                 wallet_to: str):
        payload = {
            'amount': str(amount),
            'currency': str(currency),
            'walletfrom': wallet_from,
            'walletto': wallet_to,
        }
        return self._sign_and_post('transfer', payload)

    # Allow you to request a withdrawal from one of your wallet.
    def withdraw(self,
                 w_type: str,
                 wallet: str,
                 amount: float,
                 address: str):
        payload = {
            'withdraw_type': str(w_type),
            'walletselected': wallet,
            'amount': str(amount),
            'address': address,
        }
        return self._sign_and_post('withdraw', payload)

    # ORDERS ------------------------------------------------------------------
    # Submit a new order.
    def place_order(self,
                    amount: float,
                    price: float,
                    side: str,
                    ord_type: str,
                    symbol: str,
                    params: dict=None):
        payload = {
            'symbol': str(symbol),
            'amount': str(amount),
            'price': str(price),
            'side': str(side),
            'type': str(ord_type),
            'ocoorder': False,
        }
        payload.update(params or {})
        return self._sign_and_post('order/new', payload)

    # Submit a new order.
    def place_oco_order(self,
                        amount: float,
                        price: float,
                        side: str,
                        ord_type: str,
                        symbol: str,
                        buy_price_oco: float,
                        sell_price_oco: float):
        oco = {
            'ocoorder': True,
            'buy_price_oco': str(buy_price_oco),
            'sell_price_oco': str(sell_price_oco),
        }
        return self.place_order(amount, price, side, ord_type, symbol, oco)

    # Cancel an order.
    def delete_order(self, order_id: int):
        payload = {
            'order_id': order_id,
        }
        return self._sign_and_post('order/cancel', payload)

    # Cancel all orders.
    def delete_all_order(self):
        return self._sign_and_post('order/cancel/all')

    # Get the status of an order. Is it active? Was it cancelled?
    # To what extent has it been executed? etc.
    def status_order(self, order_id: int):
        payload = {
            'order_id': order_id,
        }
        return self._sign_and_post('order/status', payload)

    # View your active orders.
    def active_orders(self):
        return self._sign_and_post('orders')

    # View your latest inactive orders.
    # Limited to last 3 days and 1 request per minute.
    def orders_history(self, limit: int):
        payload = {
            'limit': limit,
        }
        return self._sign_and_post('order/hist', payload)

    # POSITIONS ---------------------------------------------------------------
    # View your active positions.
    def active_positions(self):
        return self._sign_and_post('positions')

    # Claim a position.
    def claim_position(self, position_id: int):
        payload = {
            'position_id': position_id,
        }
        return self._sign_and_post('position/claim', payload)

    # HISTORICAL DATA ---------------------------------------------------------
    # View all of your balance ledger entries.
    def balance_history(self,
                        currency: str,
                        since: float=None,
                        until: float=None,
                        limit: int=None,
                        wallet: str=None):
        payload = {
            'currency': str(currency),
            'since': since,
            'until': until,
            'limit': limit,
            'wallet': wallet,
        }
        return self._sign_and_post('history', payload)

    # View your past deposits/withdrawals.
    def movements(self,
                  currency: str,
                  method: str=None,
                  since: float=None,
                  until: float=None,
                  limit: int=None):
        payload = {
            'currency': str(currency),
            'method': method,
            'since': since,
            'until': until,
            'limit': limit,
        }
        return self._sign_and_post('history/movements', payload)

    # View your past trades.
    def past_trades(self,
                    symbol: str,
                    timestamp: float=None,
                    until: float=None,
                    limit_trades: int=None,
                    reverse: bool=None):
        payload = {
            'symbol': str(symbol),
            'timestamp': timestamp,
            'until': until,
            'limit_trades': limit_trades,
            'reverse': reverse if reverse is not None else None,
        }
        return self._sign_and_post('mytrades', payload)

    # MARGIN FUNDING ----------------------------------------------------------
    # Submit a new Offer.
    def place_offer(self,
                    currency: str,
                    amount: float,
                    rate: float,
                    period: int,
                    direction: str):
        payload = {
            'currency': str(currency),
            'amount': str(amount),
            'rate': str(rate),
            'period': period,
            'direction': str(direction),
        }
        return self._sign_and_post('offer/new', payload)

    # Cancel an offer.
    def cancel_offer(self, offer_id: int):
        payload = {
            'offer_id': offer_id,
        }
        return self._sign_and_post('offer/cancel', payload)

    # Get the status of an offer. Is it active? Was it cancelled?
    # To what extent has it been executed? etc.
    def status_offer(self, offer_id: int):
        payload = {
            'offer_id': offer_id,
        }
        return self._sign_and_post('offer/status', payload)

    # View your active offers.
    def active_offers(self):
        return self._sign_and_post('offers')

    # PRIVATE METHODS ---------------------------------------------------------
    # Pack and sign the payload of the request.
    def _sign_payload(self, path: str, payload: dict):

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
    def _sign_and_get(self, path: str, payload: dict=None):
        url, path = self.url_path_for(path)
        signed_payload = self._sign_payload(path, payload or {})
        return self.get(url, headers=signed_payload)

    # Packs and sign the payload and send the request with POST.
    def _sign_and_post(self, path: str, payload: dict=None):
        url, path = self.url_path_for(path)
        signed_payload = self._sign_payload(path, payload or {})
        return self.post(url, headers=signed_payload, data=payload)
