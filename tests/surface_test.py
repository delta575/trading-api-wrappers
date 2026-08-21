import unittest

from trading_api_wrappers import (
    OKX,
    Binance,
    Bitfinex,
    BitfinexV2,
    Bitso,
    Bitstamp,
    Buda,
    Bybit,
    Coinbase,
    Foxbit,
    Kraken,
    MercadoBitcoin,
    NotBank,
    Orionx,
    Ripio,
)
from trading_api_wrappers.ripio.clients import RipioExchangePublic

PUBLIC = [
    "markets",
    "ticker",
    "order_book",
    "trades",
    "candles",
    "quotation",
    "quotation_market",
    "quotation_limit",
]

AUTH = [
    "balances",
    "new_order",
    "cancel_order",
    "order_details",
    "open_orders",
    "order_pages",
    "deposits",
    "withdrawals",
]

BUDA_AUTH = [
    "balance",
    "new_order",
    "cancel_order",
    "order_details",
    "order_pages",
    "open_orders",
    "deposits",
    "withdrawals",
    "withdrawal",
    "simulate_withdrawal",
    "batch_orders",
]

CLIENTS = [
    ("Buda", Buda.Public, Buda.Auth, BUDA_AUTH),
    ("Orionx", Orionx.Public, Orionx.Auth, AUTH),
    ("NotBank", NotBank.Public, NotBank.Auth, AUTH),
    ("Bitso", Bitso.Public, Bitso.Auth, AUTH),
    ("MercadoBitcoin", MercadoBitcoin.Public, MercadoBitcoin.Auth, AUTH),
    ("Foxbit", Foxbit.Public, Foxbit.Auth, AUTH),
    ("Binance", Binance.Public, Binance.Auth, AUTH),
    ("OKX", OKX.Public, OKX.Auth, AUTH),
    ("Bybit", Bybit.Public, Bybit.Auth, AUTH),
    ("Coinbase", Coinbase.Public, Coinbase.Auth, AUTH),
    ("Kraken", Kraken.Public, Kraken.Auth, [*AUTH, "simulate_withdrawal"]),
    ("Bitstamp", Bitstamp.Public, Bitstamp.Auth, AUTH),
    ("Bitfinex", Bitfinex.Public, Bitfinex.Auth, AUTH),
    ("BitfinexV2", BitfinexV2.Public, BitfinexV2.Auth, AUTH),
]


class SurfaceTest(unittest.TestCase):
    def test_public_surface(self):
        for name, public_cls, _auth_cls, _auth_names in CLIENTS:
            for method in PUBLIC:
                self.assertTrue(
                    callable(getattr(public_cls, method, None)),
                    f"{name}.Public.{method}",
                )

    def test_ripio_exchange_public_surface(self):
        for method in PUBLIC:
            if method == "candles":
                continue
            self.assertTrue(
                callable(getattr(RipioExchangePublic, method, None)),
                f"RipioExchangePublic.{method}",
            )

    def test_ripio_auth_surface(self):
        for method in AUTH:
            self.assertTrue(
                callable(getattr(Ripio.Auth, method, None)),
                f"Ripio.Auth.{method}",
            )

    def test_auth_surface(self):
        for name, _public_cls, auth_cls, auth_names in CLIENTS:
            for method in auth_names:
                self.assertTrue(
                    callable(getattr(auth_cls, method, None)),
                    f"{name}.Auth.{method}",
                )
