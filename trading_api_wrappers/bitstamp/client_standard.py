import pytz
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
    def get_pair_mapping(base, quote):
        return "%s%s" % (base.lower(), quote.lower())
