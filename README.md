# Trading API Wrappers

> Python 3.6+ clients for popular **Crypto Exchanges** and other useful services.

> **Disclaimer:** Still at an early stage of development. Rapidly evolving APIs.

[![PyPI - License](https://img.shields.io/pypi/l/trading-api-wrappers.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/trading-api-wrappers.svg)
[![PyPI](https://img.shields.io/pypi/v/trading-api-wrappers.svg)](https://pypi.org/project/trading-api-wrappers/)
![PyPI - Status](https://img.shields.io/pypi/status/trading-api-wrappers.svg)
[![Updates](https://pyup.io/repos/github/delta575/trading-api-wrappers/shield.svg)](https://pyup.io/repos/github/delta575/trading-api-wrappers/)

Supported APIs:

- [Buda](https://www.buda.com)
- [Bitfinex](https://www.bitfinex.com)
- [Bitstamp](https://www.bitstamp.net)
- [CoinDesk](https://www.coindesk.com)
- [CoinMarketCap](https://coinmarketcap.com)
- [CryptoMKT](https://www.cryptomkt.com)
- [Kraken](https://www.kraken.com)
- [OpenExchangeRates](https://openexchangerates.org)

## Installation

### Requirements

- Python 3.6+

To install, simply use `poetry` (or `pip`, of course):

```bash
$ poetry add trading-api-wrappers
```

### Dev setup

```bash
$ poetry install
```

Rename `.env.example` to `.env` and configure your credentials (for tests)

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
https://bitfinex.readme.io/v1/docs

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
https://www.kraken.com/help/api

### CoinDesk

```python
from trading_api_wrappers import CoinDesk
client = CoinDesk()
```

CoinDesk API Doc:
https://www.coindesk.com/api

### CoinMarketCap

```python
from trading_api_wrappers import CoinMarketCap
client = CoinMarketCap()
```

CoinMarketCap API Doc:
https://coinmarketcap.com/api

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

CryptoMKT API Doc:
https://developers.cryptomkt.com

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
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdelta575%2Ftrading-api-wrappers.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdelta575%2Ftrading-api-wrappers?ref=badge_shield)

The MIT License

Copyright © 2017
[Felipe Aránguiz](mailto://faranguiz575@gmail.com) | [Sebastián Aránguiz](mailto://sarang575@gmail.com)

See [LICENSE](LICENSE)

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdelta575%2Ftrading-api-wrappers.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdelta575%2Ftrading-api-wrappers?ref=badge_large)

## Donations

Bitcoin:

    186kDw9LFcPvup17YSrWZbFqdZzELUFad3

Ether:

    0xeF38fA6c0a37A1BdB60CADd7f6e71F351F6d2583
