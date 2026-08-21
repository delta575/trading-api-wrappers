from ..base import Client
from ..errors import InvalidResponse


class CoinMarketCap(Client):
    """CoinMarketCap Pro API client (keyless public-api by default)."""

    timeout = 30
    error_keys = []

    def __init__(self, api_key: str | None = None, **kwargs):
        base_url = (
            "https://pro-api.coinmarketcap.com/"
            if api_key
            else "https://pro-api.coinmarketcap.com/public-api/"
        )
        super().__init__(base_url=base_url, **kwargs)
        self.api_key = api_key
        self.session.headers["Accept"] = "application/json"
        if api_key:
            self.session.headers["X-CMC_PRO_API_KEY"] = api_key

    def _decode_response(self, response):
        payload = super()._decode_response(response)
        status = payload.get("status") if isinstance(payload, dict) else None
        if status:
            error_code = str(status.get("error_code", "0"))
            if error_code not in ("0", "None", "null"):
                raise InvalidResponse(status.get("error_message") or error_code, response)
        return payload

    def _quote_price(self, item: dict, convert: str) -> float:
        quotes = item.get("quote") or []
        convert = convert.upper()
        if isinstance(quotes, dict):
            return float(quotes[convert]["price"])
        for quote in quotes:
            if str(quote.get("symbol", "")).upper() == convert:
                return float(quote["price"])
        raise KeyError(convert)

    def _pick_symbol(self, items, symbol: str):
        matches = [
            item
            for item in items
            if str(item.get("symbol", "")).upper() == symbol.upper()
        ]
        if not matches:
            raise KeyError(symbol)
        matches.sort(key=lambda item: item.get("cmc_rank") or item.get("rank") or 10**9)
        return matches[0]

    def map_symbol(self, symbol: str) -> dict:
        data = self.get("v1/cryptocurrency/map", params={"symbol": symbol.upper()})["data"]
        return self._pick_symbol(data, symbol)

    def ticker(
        self,
        currency: str | None = None,
        convert: str | None = None,
        start: int | None = None,
        limit: int | None = None,
    ):
        convert = (convert or "USD").upper()
        if currency:
            payload = self.get(
                "v3/cryptocurrency/quotes/latest",
                params={"symbol": currency.upper(), "convert": convert},
            )
            data = payload["data"]
            items = data if isinstance(data, list) else list(data.values())
            flat = []
            for item in items:
                if isinstance(item, list):
                    flat.extend(item)
                else:
                    flat.append(item)
            return self._pick_symbol(flat, currency)
        params = {
            "convert": convert,
            "start": start or 1,
            "limit": limit or 100,
        }
        return self.get("v3/cryptocurrency/listings/latest", params=params)["data"]

    def price(self, currency: str, convert: str | None = None):
        convert = (convert or "USD").upper()
        ticker = self.ticker(currency, convert)
        return self._quote_price(ticker, convert)

    def stats(self, convert: str | None = None):
        convert = (convert or "USD").upper()
        return self.get(
            "v1/global-metrics/quotes/latest",
            params={"convert": convert},
        )["data"]
