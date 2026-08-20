# Trading API Wrappers

Python 3.10+ clients for popular **crypto exchanges** and related services.

> **Disclaimer:** Some upstream APIs have changed or shut down since this
> library was first written. See [API status](#api-status) below.

[![PyPI - License](https://img.shields.io/pypi/l/trading-api-wrappers.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/trading-api-wrappers.svg)
[![PyPI](https://img.shields.io/pypi/v/trading-api-wrappers.svg)](https://pypi.org/project/trading-api-wrappers/)
![PyPI - Status](https://img.shields.io/pypi/status/trading-api-wrappers.svg)

## API status

| Client | Public API | Notes |
| --- | --- | --- |
| Buda | Active | Markets updated (SOL, USDT). ARS pairs removed. |
| Bitfinex v1 / v2 | Active | v2 authenticated client is not implemented. |
| Bitstamp | Active | |
| Kraken | Active | |
| SFOX | Active | |
| Bitcoinity | Active | |
| Ripio rates | Active | Exchange order-book client is deprecated. |
| Open Exchange Rates | Active | Requires an app id. |
| CurrencyLayer | Active | Requires an access key. |
| CoinDesk | **Deprecated** | BPI host `api.coindesk.com` is gone. |
| CoinMarketCap | **Deprecated** | Public v1 API was shut down. |
| CryptoMKT | **Deprecated** | v1 API is retired; migrate to exchange API v3. |
| Bitex | **Deprecated** | `bitex.la` is gone. |
| SURBTC | **Deprecated** | Rebranded to Buda years ago. Use `Buda`. |

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
from trading_api_wrappers import Bitfinex
client = Bitfinex.Public()
```

Authenticated API:

```python
from trading_api_wrappers import Bitfinex
client = Bitfinex.Auth(API_KEY, API_SECRET)
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

### CoinDesk

```python
from trading_api_wrappers import CoinDesk
client = CoinDesk()
```

Deprecated: the public BPI API is no longer available.

### CoinMarketCap

```python
from trading_api_wrappers import CoinMarketCap
client = CoinMarketCap()
```

Deprecated: the public v1 API was shut down. Use the [CoinMarketCap Pro API](https://coinmarketcap.com/api/).

### CryptoMKT

```python
from trading_api_wrappers import CryptoMKT
client = CryptoMKT.Public()
```

Deprecated: API v1 returns `This API is deprecated, please change to api.exchange.cryptomkt.com`.

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
