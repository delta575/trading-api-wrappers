# Trading API Wrappers

LATAM-first Python clients for **crypto trading and market data**. The
library wraps the exchanges a bot actually needs in Chile, Mexico, and
Brazil, plus a short list of global venues for USD/USDT price.

It is not a CCXT clone. Coverage is intentional: a handful of venues with
working books, not twenty thin wrappers.

[![PyPI - License](https://img.shields.io/pypi/l/trading-api-wrappers.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/trading-api-wrappers.svg)
[![PyPI](https://img.shields.io/pypi/v/trading-api-wrappers.svg)](https://pypi.org/project/trading-api-wrappers/)
![PyPI - Status](https://img.shields.io/pypi/status/trading-api-wrappers.svg)

## Coverage

Native pair ids are used as-is (`BTCCLP`, `btc_mxn`, `BTC-BRL`, `btcbrl`,
`BTCUSDT`). Public clients expose `markets()`, `ticker()`, `order_book()`,
and `trades()`.

### LATAM

| Client | Quote | Notes |
| --- | --- | --- |
| Buda | CLP | Chilean CEX. SOL and USDT markets. |
| Orionx | CLP | The other live Chilean CEX. GraphQL; **signed requests required** for books. |
| NotBank | CLP / USDT | Successor of CryptoMKT. AlphaPoint `/AP` REST. |
| Bitso | MXN | Mexican CEX. REST v3 public books. |
| Mercado Bitcoin | BRL | The BRL book that matters. Data API v4 + TAPI. |
| Foxbit | BRL | Second BRL venue, Pix rails. REST v3. |
| Ripio | BRL | Retail rates plus Ripio Trade v4 public books. |

`CryptoMKT` remains imported as a **compatibility alias of NotBank**. The
old `api.exchange.cryptomkt.com` host is not a venue.

### Global

| Client | Notes |
| --- | --- |
| Binance | Spot v3 ticker/book. Some regions return HTTP 451. |
| OKX | REST v5. |
| Bybit | v5 spot. Some regions return HTTP 403. |
| Coinbase | Coinbase Exchange (`api.exchange.coinbase.com`), the USD book. |
| Kraken | |
| Bitfinex | v1 / v2; v2 authenticated client included. |
| Bitstamp | |

### Data helpers

CoinMarketCap (keyless public API, or Pro with `api_key`), Open Exchange
Rates, CurrencyLayer.

Removed in 0.20.0: SFOX and Bitcoinity. Removed in 0.19.0: CoinDesk BPI,
Bitex, and the SURBTC alias (use `Buda`).

Not in scope: MEXC, Gate, Bitget, KuCoin, HTX, Lemon Cash, or other retail
apps without an order book. Use CCXT there.

## Installation

### Requirements

- Python 3.10+

To install, use `poetry` (or `pip`):

```bash
$ poetry add trading-api-wrappers
```

```bash
$ pip install trading-api-wrappers
```

### Dev setup

```bash
$ poetry install
```

Copy `.env.example` to `.env` and fill in credentials if you want to run
authenticated tests. Public tests skip auth classes when keys are missing.
Tests skip HTTP 403/451 when a host geo-blocks the runner.

```bash
$ poetry run pytest
$ poetry run ruff check .
```

## Usage

Public clients share the same shape:

```python
from trading_api_wrappers import Bitso, Buda, MercadoBitcoin, NotBank

buda = Buda.Public()
buda.ticker("BTC-CLP")

notbank = NotBank.Public()
notbank.order_book("BTCCLP")

bitso = Bitso.Public()
bitso.order_book("btc_mxn")

mb = MercadoBitcoin.Public()
mb.order_book("BTC-BRL")
```

Authenticated clients take the venue's native credentials:

```python
from trading_api_wrappers import Bitso, NotBank, Orionx

orionx = Orionx.Auth(API_KEY, API_SECRET)          # required for CLP books
notbank = NotBank.Auth(API_KEY, API_SECRET, USER_ID)
bitso = Bitso.Auth(API_KEY, API_SECRET)
```

### Buda

```python
from trading_api_wrappers import Buda
client = Buda.Public()
client = Buda.Auth(API_KEY, API_SECRET)
```

https://api.buda.com

### Orionx

```python
from trading_api_wrappers import Orionx
client = Orionx.Auth(API_KEY, API_SECRET)
book = client.order_book("BTCCLP")
```

https://docs.orionx.com

### NotBank (CryptoMKT)

```python
from trading_api_wrappers import NotBank
client = NotBank.Public()
client = NotBank.Auth(API_KEY, API_SECRET, USER_ID)
```

`CryptoMKT.Public()` still works and warns; it is NotBank.

https://api.notbank.exchange

### Bitso

```python
from trading_api_wrappers import Bitso
client = Bitso.Public()
ticker = client.ticker("btc_mxn")
```

https://docs.bitso.com

### Mercado Bitcoin

```python
from trading_api_wrappers import MercadoBitcoin
client = MercadoBitcoin.Public()
book = client.order_book("BTC-BRL")
auth = MercadoBitcoin.Auth(TAPI_ID, TAPI_SECRET)
```

https://www.mercadobitcoin.com.br/api-doc

### Foxbit

```python
from trading_api_wrappers import Foxbit
client = Foxbit.Public()
book = client.order_book("btcbrl")
```

https://docs.foxbit.com.br

### Ripio

```python
from trading_api_wrappers import Ripio
client = Ripio.Public()
rates = client.rates()
book = client.exchange.order_book("BTC_BRL")
```

### Binance / OKX / Bybit / Coinbase

```python
from trading_api_wrappers import Binance, Bybit, Coinbase, OKX

Binance.Public().ticker("BTCUSDT")
OKX.Public().order_book("BTC-USDT")
Bybit.Public().ticker("BTCUSDT")
Coinbase.Public().order_book("BTC-USD")
```

Coinbase Exchange auth also needs a passphrase. OKX auth needs a passphrase.

### Bitfinex

```python
from trading_api_wrappers import Bitfinex, BitfinexV2
client = Bitfinex.Public()
client_v2 = BitfinexV2.Auth(API_KEY, API_SECRET)
```

https://docs.bitfinex.com/docs

### Bitstamp

```python
from trading_api_wrappers import Bitstamp
client = Bitstamp.Public()
client = Bitstamp.Auth(API_KEY, API_SECRET, CUSTOMER_ID)
```

https://www.bitstamp.net/api

### Kraken

```python
from trading_api_wrappers import Kraken
client = Kraken.Public()
client = Kraken.Auth(API_KEY, API_SECRET)
```

https://docs.kraken.com/api/

### CoinMarketCap

```python
from trading_api_wrappers import CoinMarketCap
client = CoinMarketCap()                 # keyless public API
client = CoinMarketCap(api_key=API_KEY)  # Pro API
```

https://coinmarketcap.com/api/

### OpenExchangeRates

```python
from trading_api_wrappers import OXR
client = OXR(APP_ID)
```

https://docs.openexchangerates.org

### CurrencyLayer

```python
from trading_api_wrappers import CurrencyLayer
client = CurrencyLayer(ACCESS_KEY)
```

https://currencylayer.com/documentation

## Licence

[![PyPI - License](https://img.shields.io/pypi/l/trading-api-wrappers.svg)](https://opensource.org/licenses/MIT)

The MIT License

Copyright © 2017-2026
[Felipe Aránguiz](mailto://faranguiz575@gmail.com) | [Sebastián Aránguiz](mailto://sarang575@gmail.com)

See [LICENSE](LICENSE)
