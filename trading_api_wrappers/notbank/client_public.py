"""NotBank public REST client (AlphaPoint /AP). Successor of CryptoMKT."""

from __future__ import annotations

import json

from ..base import Client, ModelMixin
from ..errors import InvalidResponse
from ..market import Candlestick, Market, OrderBook, OrderBookEntry, Ticker, Trade
from ..trading import BookQuotationMixin

# AlphaPoint GetL2Snapshot row:
# MDUpdateID, Accounts, ActionDateTime, ActionType, LastTradePrice,
# NumberOfOrders, Price, ProductPairCode, Quantity, Side (0=bid, 1=ask)
_L2_PRICE = 6
_L2_QTY = 8
_L2_SIDE = 9
_L2_TS = 2

# GetLastTrades row (typical):
# TradeId, InstrumentId, Quantity, Price, Order1, Order2, Timestamp, Direction
_T_ID = 0
_T_QTY = 2
_T_PRICE = 3
_T_TS = 6
_T_SIDE = 7


class NotBankPublic(BookQuotationMixin, Client, ModelMixin):
    """NotBank public market data. POST JSON to /AP/{Method}."""

    base_url = "https://api.notbank.exchange/AP/"
    error_keys = ["errormsg"]
    oms_id = 1

    def __init__(self, timeout: int | None = None, oms_id: int | None = None, **kwargs):
        super().__init__(timeout, **kwargs)
        if oms_id is not None:
            self.oms_id = oms_id
        self._markets_by_symbol: dict[str, Market] | None = None

    def _call(self, method: str, payload: dict | None = None):
        body = {"OMSId": self.oms_id, **(payload or {})}
        return self.post(method, json=body)

    def _decode_response(self, response):
        if not response.content:
            return []
        payload = super()._decode_response(response)
        if isinstance(payload, dict) and payload.get("result") is False:
            raise InvalidResponse(payload.get("errormsg") or str(payload), response)
        return payload

    def _parse_level1(self, items):
        parsed = []
        for item in items or []:
            if isinstance(item, str):
                item = json.loads(item)
            parsed.append(item)
        return parsed

    def instruments(self):
        return self._call("GetInstruments")

    def markets(self):
        items = self.instruments()
        if self.return_json:
            return items
        markets = []
        for item in items:
            markets.append(
                Market.create(
                    item.get("Symbol"),
                    item.get("Product1Symbol"),
                    item.get("Product2Symbol"),
                    item,
                )
            )
        self._markets_by_symbol = {market.id.upper(): market for market in markets}
        return markets

    def _market(self, symbol: str) -> Market:
        symbol = str(symbol).upper()
        mapping = self._markets_by_symbol
        if mapping is None:
            previous = self.return_json
            self.return_json = False
            try:
                self.markets()
            finally:
                self.return_json = previous
            mapping = self._markets_by_symbol or {}
        market = mapping.get(symbol)
        if market is None:
            raise KeyError(symbol)
        return market

    def _instrument_id(self, symbol: str) -> int:
        market = self._market(symbol)
        return int(market.json["InstrumentId"])

    def level1(self, symbol: str):
        instrument_id = self._instrument_id(symbol)
        return self._call("GetLevel1", {"InstrumentId": instrument_id})

    def ticker(self, symbol: str = "BTCCLP"):
        data = self.level1(symbol)
        if self.return_json:
            return data
        return Ticker.create(
            data,
            symbol=str(symbol).upper(),
            last=data.get("LastTradedPx"),
            bid=data.get("BestBid"),
            ask=data.get("BestOffer"),
            volume=data.get("Rolling24HrVolume"),
            timestamp=data.get("LastTradeTime") or data.get("TimeStamp"),
        )

    def order_book(self, symbol: str = "BTCCLP", depth: int = 20):
        instrument_id = self._instrument_id(symbol)
        rows = self._call(
            "GetL2Snapshot",
            {"InstrumentId": instrument_id, "Depth": depth},
        )
        if self.return_json:
            return rows
        bids = []
        asks = []
        timestamp = None
        for row in rows:
            entry = OrderBookEntry(price=float(row[_L2_PRICE]), amount=float(row[_L2_QTY]))
            if int(row[_L2_SIDE]) == 1:
                asks.append(entry)
            else:
                bids.append(entry)
            timestamp = row[_L2_TS]
        return OrderBook(bids=bids, asks=asks, timestamp=timestamp, json=rows)

    def trades(self, symbol: str = "BTCCLP", limit: int = 20):
        instrument_id = self._instrument_id(symbol)
        rows = self._call(
            "GetLastTrades",
            {"InstrumentId": instrument_id, "Count": limit},
        )
        if self.return_json:
            return rows
        trades = []
        for row in rows:
            side = row[_T_SIDE] if len(row) > _T_SIDE else None
            trades.append(
                Trade.create(
                    row,
                    trade_id=row[_T_ID],
                    price=row[_T_PRICE],
                    amount=row[_T_QTY],
                    side=side,
                    timestamp=row[_T_TS] if len(row) > _T_TS else None,
                )
            )
        return trades

    def candles(
        self,
        symbol: str = "BTCCLP",
        interval: int = 60,
        from_date: int | None = None,
        to_date: int | None = None,
    ):
        import time

        instrument_id = self._instrument_id(symbol)
        now_ms = int(time.time() * 1000)
        payload = {
            "InstrumentId": instrument_id,
            "Interval": interval,
            "FromDate": from_date or (now_ms - 86_400_000),
            "ToDate": to_date or now_ms,
        }
        rows = self._call("GetTickerHistory", payload)
        if self.return_json:
            return rows
        candles = []
        for row in rows or []:
            if isinstance(row, (list, tuple)) and len(row) >= 5:
                candles.append(
                    Candlestick.create(
                        row,
                        timestamp=row[0],
                        open_price=row[1],
                        high=row[2],
                        low=row[3],
                        close=row[4],
                        volume=row[5] if len(row) > 5 else None,
                    )
                )
            elif isinstance(row, dict):
                candles.append(
                    Candlestick.create(
                        row,
                        timestamp=row.get("DateTime") or row.get("timestamp"),
                        open_price=row.get("Open") or row.get("open"),
                        high=row.get("High") or row.get("high"),
                        low=row.get("Low") or row.get("low"),
                        close=row.get("Close") or row.get("close"),
                        volume=row.get("Volume") or row.get("volume"),
                    )
                )
        return candles
