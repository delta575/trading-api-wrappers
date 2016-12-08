import requests
import json
import base64
import hmac
import hashlib
import time

URL = 'https://api.bitfinex.com/v1'


# unauthenticated

class Bitfinex(object):
    def __init__(self, key='', secret=''):
        self.api_key = key
        self.api_secret = secret

    def ticker(self, symbol='btcusd'):  # gets the innermost bid and asks and information on the most recent trade.
        try:
            rep = requests.get(URL + "/pubticker/" + symbol, verify=True).json()
            rep['last_price']
            return rep

        except:
            return 'error'

    def stats(self, symbol='btcusd'):  # Various statistics about the requested pairs.
        try:
            r = requests.get(URL + "/stats/" + symbol, verify=True)
            rep = r.json()
            rep['volume']
            return rep

        except KeyError:
            return rep['message']

    def today(self, symbol='btcusd'):  # today's low, high and volume.

        r = requests.get(URL + "/today/" + symbol, verify=True)
        rep = r.json()

        try:
            rep['volume']
        except KeyError:
            return rep['message']

        return rep

    def orderbook(self, symbol='btcusd'):  # get the full order book.

        r = requests.get(URL + '/book/' + symbol, verify=True)
        rep = r.json()

        return rep

    def lendbook(self, currency='btc'):  # get the full lend book.

        r = requests.get(URL + "/lendbook/" + currency, verify=True)
        rep = r.json()

        return rep

    def trades(self, symbol='btcusd'):  # get a list of the most recent trades for the given symbol.

        r = requests.get(URL + "/trades/" + symbol, verify=True)
        rep = r.json()

        return rep

    def lends(self, currency='btc'):
        # get a list of the most recent lending data for the given currency:
        # total amount lent and rate (in % by 365 days).

        r = requests.get(URL + "/lends/" + currency, verify=True)
        rep = r.json()

        return rep

    def symbols(self):  # get a list of valid symbol IDs.

        r = requests.get(URL + "/symbols", verify=True)
        rep = r.json()

        return rep

    # authenticated

    def genNonce(self):  # generates a nonce, used for authentication.
        return str((time.time() * 1000000))

    def payloadPacker(self, payload):  # packs and signs the payload of the request.

        j = json.dumps(payload).encode('utf-8')
        data = base64.standard_b64encode(j)

        h = hmac.new(self.api_secret.encode('utf-8'), data, hashlib.sha384)
        signature = h.hexdigest()

        return {
            "X-BFX-APIKEY": self.api_key,
            "X-BFX-SIGNATURE": signature,
            "X-BFX-PAYLOAD": data
        }

    def place_order(self, amount, price, side, ord_type, symbol='btcusd', exchange='bitfinex',
                    params=None):  # submit a new order.

        payload = {

            "request": "/v1/order/new",
            "nonce": self.genNonce(),
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "exchange": exchange,
            "side": side,
            "type": ord_type

        }

        if params:
            keys = list(params.keys())
            for k in keys:
                payload[k] = params[k]

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/order/new", headers=signed_payload, data=json.dumps(payload), verify=True)
        rep = r.json()

        try:
            rep['order_id']
        except:
            return rep['message']

        return rep

    def delete_order(self, order_id):  # cancel an order.

        payload = {

            "request": "/v1/order/cancel",
            "nonce": self.genNonce(),
            "order_id": order_id

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/order/cancel", headers=signed_payload, verify=True)
        rep = r.json()

        try:
            rep['avg_excution_price']
        except:
            return rep['message']

        return rep

    def delete_all_order(self):  # cancel an order.

        payload = {

            "request": "/v1/order/cancel/all",
            "nonce": self.genNonce(),

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/order/cancel/all", headers=signed_payload, verify=True)
        rep = r.json()
        return rep

    '''
        try:
            rep['avg_excution_price']
        except:
            return rep['message']
    '''

    def status_order(self, order_id):
        # get the status of an order. Is it active? Was it cancelled? To what extent has it been executed? etc.

        payload = {

            "request": "/v1/order/status",
            "nonce": self.genNonce(),
            "order_id": order_id

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/order/status", headers=signed_payload, verify=True)
        rep = r.json()

        try:
            rep['avg_excution_price']
        except:
            return rep['message']

        return rep

    def active_orders(self):  # view your active orders.

        payload = {

            "request": "/v1/orders",
            "nonce": self.genNonce()

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/orders", headers=signed_payload, verify=True)
        rep = r.json()

        return rep

    def active_positions(self):  # view your active positions.

        payload = {

            "request": "/v1/positions",
            "nonce": self.genNonce()

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/positions", headers=signed_payload, verify=True)
        rep = r.json()

        return rep

    def claim_position(self, position_id):  # Claim a position.

        payload = {

            "request": "/v1/position/claim",
            "nonce": self.genNonce(),
            "position_id": position_id

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/position/claim", headers=signed_payload, verify=True)
        rep = r.json()

        return rep

    def past_trades(self, timestamp=0, symbol='btcusd'):  # view your past trades

        payload = {

            "request": "/v1/mytrades",
            "nonce": self.genNonce(),
            "symbol": symbol,
            "timestamp": timestamp

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/mytrades", headers=signed_payload, verify=True)
        rep = r.json()

        return rep

    def place_offer(self, currency, amount, rate, period, direction):

        payload = {

            "request": "/v1/offer/new",
            "nonce": self.genNonce(),
            "currency": currency,
            "amount": amount,
            "rate": rate,
            "period": period,
            "direction": direction

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/offer/new", headers=signed_payload, verify=True)
        rep = r.json()

        return rep

    def cancel_offer(self, offer_id):

        payload = {

            "request": "/v1/offer/cancel",
            "nonce": self.genNonce(),
            "offer_id": offer_id

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/offer/cancel", headers=signed_payload, verify=True)
        rep = r.json()

        return rep

    def status_offer(self, offer_id):

        payload = {

            "request": "/v1/offer/status",
            "nonce": self.genNonce(),
            "offer_id": offer_id

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/offer/status", headers=signed_payload, verify=True)
        rep = r.json()

        return rep

    def active_offers(self):

        payload = {

            "request": "/v1/offers",
            "nonce": self.genNonce()

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/offers", headers=signed_payload, verify=True)
        rep = r.json()

        return rep

    def balances(self):  # see your balances.

        payload = {

            "request": "/v1/balances",
            "nonce": self.genNonce()

        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/balances", headers=signed_payload, verify=True)
        rep = r.json()

        return rep

    def movements(self, currency, params=None):  # View your past deposits/withdrawals.

        payload = {

            "request": "/v1/history/movements",
            "nonce": self.genNonce(),
            "currency": currency
        }

        if params:
            keys = list(params.keys())
            for k in keys:
                payload[k] = params[k]

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/history/movements", headers=signed_payload, verify=True)
        rep = r.json()

        return rep

    def withdraw(self, amount, currency, wallet, address):

        payload = {

            "request": "/v1/withdraw",
            "nonce": self.genNonce(),
            "amount": str(amount),
            "withdraw_type": currency,
            "walletselected": wallet,
            "address": address
        }

        signed_payload = self.payloadPacker(payload)
        r = requests.post(URL + "/withdraw", headers=signed_payload, data=json.dumps(payload), verify=True)
        rep = r.json()
        return rep

    def key_info(self):
        payload = {

            "request": "/v1/key_info",
            "nonce": self.genNonce(),
        }

        signed_payload = self.payloadPacker(payload)
        r = requests.get(URL + "/key_info", headers=signed_payload, verify=True)
        print(r)
        rep = r.json()
        return rep
