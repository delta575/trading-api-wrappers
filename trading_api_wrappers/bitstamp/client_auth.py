import hashlib
import hmac

# local
from ..common import check_keys, clean_parameters, gen_nonce
from .client_public import BitstampPublic



class BitstampAuth(BitstampPublic):

    def __init__(self, key, secret, customer_id, timeout=30):
        BitstampPublic.__init__(self, timeout)
        check_keys(key, secret)
        self.key = str(key)
        self.secret = str(secret)
        self.customer_id = str(customer_id)

    # Private user data -------------------------------------------------------
    # Get account balance.
    def balance(self):
        url, path = self.url_path_for('balance/')
        payload = {
            'nonce': 0
        }
        return self._sign_and_post(url, path, payload)

    # PRIVATE METHODS ---------------------------------------------------------
    def _sign_payload(self, path, data=None):
        data['nonce'] = gen_nonce()
        msg = str(data['nonce']) + self.customer_id + self.key
        data['key'] = self.key
        signature = hmac.new(
            self.secret.encode('utf-8'),
            msg=msg.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()
        data['signature'] = signature
        return data

    def _encode_data(self, data):
        return data


    # Packs and sign the payload and send the request with POST.
    def _sign_and_post(self, url, path, payload):
        clean_payload = clean_parameters(payload)
        new_data = self._sign_payload(path, clean_payload)
        return self.post(url, headers=None, data=new_data)
