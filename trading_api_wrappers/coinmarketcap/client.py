from ..base import Client


class CoinMarketCap(Client):
    base_url = "https://api.coinmarketcap.com/v1/"
    currencies = None
    timeout = 120

    def ticker(
        self,
        currency: str = None,
        convert: str = None,
        start: int = None,
        limit: int = None,
    ):
        params = {
            "start": start,
            "limit": limit,
            "convert": convert,
        }
        if currency:
            if len(currency) == 3:
                currency = self._get_symbol(currency)["value"]
            data = self.get(f"ticker/{currency}/", params=params)[0]
        else:
            data = self.get("ticker/", params=params)
        return data

    def price(self, currency: str, convert: str = None):
        ticker = self.ticker(currency, convert)
        return float(ticker[f"price_{convert or 'usd'}".lower()])

    def stats(self, convert: str = None):
        data = self.get("global/", params={"convert": convert})
        return data

    def _get_currencies(self):
        ticker = self.ticker()
        return {
            currency["symbol"]: dict(value=currency["id"], decimals=8)
            for currency in ticker
        }

    def _get_symbol(self, currency: str):
        if self.currencies is None:
            self.currencies = self._get_currencies()
        return self.currencies[currency.upper()]
