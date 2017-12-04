# Trading API Wrappers
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Updates](https://pyup.io/repos/github/delta575/trading-api-wrappers/shield.svg)](https://pyup.io/repos/github/delta575/trading-api-wrappers/)
[![Python 3](https://pyup.io/repos/github/delta575/trading-api-wrappers/python-3-shield.svg)](https://pyup.io/repos/github/delta575/trading-api-wrappers/)

Trading API Wrappers.
Tested on Python 3.6

- [Bitfinex](https://www.bitfinex.com)
- [Kraken](https://www.kraken.com)
- [SURBTC](https://www.surbtc.com)
- [CoinDesk](https://www.coindesk.com)
- [CryptoMKT](https://www.cryptomkt.com)

## Dev setup

Install the libs

```bash
$ pip install -r requirements.txt
```

Rename `.env.example` to `.env`

## Installation

```bash
$ pip install git+https://github.com/delta575/trading-api-wrappers.git
```    

## Usage

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

### SURBTC

Public API:

```python
from trading_api_wrappers import SURBTC
client = SURBTC.Public()
```    

Authenticated API:

```python
from trading_api_wrappers import SURBTC
client = SURBTC.Auth(API_KEY, API_SECRET)
```

SURBTC API Doc:
https://api.surbtc.com

### CoinDesk

```python
from trading_api_wrappers import CoinDesk
client = CoinDesk()
```
      
Coindesk API Doc:
https://www.coindesk.com/api

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

## Licence
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The MIT License

Copyright © 2017
[Felipe Aránguiz](mailto://faranguiz575@gmail.com) | [Sebastián Aránguiz](mailto://sarang575@gmail.com)

See [LICENSE](LICENSE)

## Donations

Bitcoin:

    186kDw9LFcPvup17YSrWZbFqdZzELUFad3

Ether:

    0xeF38fA6c0a37A1BdB60CADd7f6e71F351F6d2583
