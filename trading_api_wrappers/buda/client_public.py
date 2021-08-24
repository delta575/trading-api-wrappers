from datetime import datetime

from . import constants as _c
from . import models as _m
from ..base import Client, ModelMixin


class BudaPublic(Client, ModelMixin):
    base_url = "https://www.buda.com/api/v2/"
    error_keys = ["message"]

    def markets(self):
        data = self.get("markets")
        if self.return_json:
            return data
        return [_m.Market.create_from_json(market) for market in data["markets"]]

    def market_details(self, market_id: str):
        data = self.get(f"markets/{market_id}")
        if self.return_json:
            return data
        return _m.Market.create_from_json(data["market"])

    def ticker(self, market_id: str):
        data = self.get(f"markets/{market_id}/ticker")
        if self.return_json:
            return data
        return _m.Ticker.create_from_json(data["ticker"])

    def order_book(self, market_id: str):
        data = self.get(f"markets/{market_id}/order_book")
        if self.return_json:
            return data
        return _m.OrderBook.create_from_json(data["order_book"])

    def trades(self, market_id: str, timestamp: int = None, limit: int = None):
        data = self.get(
            f"markets/{market_id}/trades",
            params={
                "timestamp": timestamp,
                "limit": limit,
            },
        )
        if self.return_json:
            return data
        return _m.Trades.create_from_json(data["trades"])

    def quotation(
        self, market_id: str, quotation_type: str, amount: float, limit: float = None
    ):
        data = self.post(
            f"markets/{market_id}/quotations",
            json={
                "quotation": {
                    "type": str(quotation_type),
                    "amount": str(amount),
                    "limit": str(limit) if limit else None,
                },
            },
        )
        if self.return_json:
            return data
        return _m.Quotation.create_from_json(data["quotation"])

    def quotation_market(self, market_id: str, quotation_type: str, amount: float):
        return self.quotation(market_id, quotation_type, amount, limit=None)

    def quotation_limit(
        self, market_id: str, quotation_type: str, amount: float, limit: float
    ):
        return self.quotation(market_id, quotation_type, amount, limit)

    def _report(
        self,
        market_id: str,
        report_type: _c.ReportType,
        start_at: datetime = None,
        end_at: datetime = None,
    ):
        if isinstance(start_at, datetime):
            start_at = int(start_at.timestamp())
        if isinstance(end_at, datetime):
            end_at = int(end_at.timestamp())
        data = self.get(
            f"markets/{market_id}/reports",
            params={
                "report_type": str(report_type),
                "from": start_at,
                "to": end_at,
            },
        )
        return data

    def report_average_prices(
        self, market_id: str, start_at: datetime = None, end_at: datetime = None
    ):
        data = self._report(market_id, _c.ReportType.AVERAGE_PRICES, start_at, end_at)
        if self.return_json:
            return data
        return [_m.AveragePrice.create_from_json(report) for report in data["reports"]]

    def report_candlestick(
        self, market_id: str, start_at: datetime = None, end_at: datetime = None
    ):
        data = self._report(market_id, _c.ReportType.CANDLESTICK, start_at, end_at)
        if self.return_json:
            return data
        return [_m.Candlestick.create_from_json(report) for report in data["reports"]]
