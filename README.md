# Trading API Wrappers

Python 3.10+ clients for popular **crypto exchanges** and related services.

[![PyPI - License](https://img.shields.io/pypi/l/trading-api-wrappers.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/trading-api-wrappers.svg)
[![PyPI](https://img.shields.io/pypi/v/trading-api-wrappers.svg)](https://pypi.org/project/trading-api-wrappers/)
![PyPI - Status](https://img.shields.io/pypi/status/trading-api-wrappers.svg)

## API status

| Client | Public API | Notes |
| --- | --- | --- |
| Buda | Active | Markets include SOL and USDT. |
| Bitfinex v1 / v2 | Active | v2 authenticated client is implemented. |
| Bitstamp | Active | |
| Kraken | Active | |
| SFOX | Active | |
| Bitcoinity | Active | |
| Ripio | Active | Retail rates plus Ripio Trade v4 public books. |
| Open Exchange Rates | Active | Requires an app id. |
| CurrencyLayer | Active | Requires an access key. |
| CoinMarketCap | Active | Keyless public API by default; pass `api_key` for Pro. |
| CryptoMKT | Active | Exchange API v3 (`api.exchange.cryptomkt.com`). |

Removed in 0.19.0: CoinDesk BPI, Bitex (`bitex.la`), and the SURBTC alias (use `Buda`).

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

```bash
$ poetry run pytest
$ poetry run ruff check .
```

## Usage

### Buda

Public API:

```python
from trading_api_wrappers import Buda
client = Buda.Public()
```

Authenticated API:

```python
from trading_api_wrappers import Buda
client = Buda.Auth(API_KEY, API_SECRET)
```

Buda API Doc:
https://api.buda.com

### Bitfinex

Public API:

```python
from trading_api_wrappers import Bitfinex, BitfinexV2
client = Bitfinex.Public()
client_v2 = BitfinexV2.Public()
```

Authenticated API:

```python
from trading_api_wrappers import Bitfinex, BitfinexV2
client = Bitfinex.Auth(API_KEY, API_SECRET)
client_v2 = BitfinexV2.Auth(API_KEY, API_SECRET)
```

Bitfinex API Doc:
https://docs.bitfinex.com/docs

### Bitstamp

Public API:

```python
from trading_api_wrappers import Bitstamp
client = Bitstamp.Public()
```

Authenticated API:

```python
from trading_api_wrappers import Bitstamp
client = Bitstamp.Auth(API_KEY, API_SECRET, CUSTOMER_ID)
```

Bitstamp API Doc:
https://www.bitstamp.net/api

### Kraken

Public API:

```python
from trading_api_wrappers import Kraken
client = Kraken.Public()
```

Authenticated API:

```python
from trading_api_wrappers import Kraken
client = Kraken.Auth(API_KEY, API_SECRET)
```

Kraken API Doc:
https://docs.kraken.com/api/

### CoinMarketCap

```python
from trading_api_wrappers import CoinMarketCap
client = CoinMarketCap()                 # keyless public API
client = CoinMarketCap(api_key=API_KEY)  # Pro API
```

CoinMarketCap API Doc:
https://coinmarketcap.com/api/

### CryptoMKT

Public API:

```python
from trading_api_wrappers import CryptoMKT
client = CryptoMKT.Public()
```

Authenticated API:

```python
from trading_api_wrappers import CryptoMKT
client = CryptoMKT.Auth(API_KEY, API_SECRET)
```

CryptoMarket API Doc:
https://api.exchange.cryptomkt.com/

### Ripio

```python
from trading_api_wrappers import Ripio
client = Ripio.Public()
rates = client.rates()
book = client.exchange.order_book("BTC_BRL")
```

### OpenExchangeRates

```python
from trading_api_wrappers import OXR
client = OXR(APP_ID)
```

OpenExchangeRates API Doc:
https://docs.openexchangerates.org

### CurrencyLayer

```python
from trading_api_wrappers import CurrencyLayer
client = CurrencyLayer(ACCESS_KEY)
```

CurrencyLayer API Doc:
https://currencylayer.com/documentation

## Licence

[![PyPI - License](https://img.shields.io/pypi/l/trading-api-wrappers.svg)](https://opensource.org/licenses/MIT)

The MIT License

Copyright © 2017-2026
[Felipe Aránguiz](mailto://faranguiz575@gmail.com) | [Sebastián Aránguiz](mailto://sarang575@gmail.com)

See [LICENSE](LICENSE)
