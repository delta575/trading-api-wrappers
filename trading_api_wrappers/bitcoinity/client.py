from ..base import Client


class Bitcoinity(Client):
    base_url = "https://bitcoinity.org/"
    timeout = 15

    def ticker(self, currency: str, exchange: str, span: str):
        return self.get(
            "markets/get_ticker",
            params={
                "currency": currency,
                "exchange": exchange,
                "span": span,
            },
        )
