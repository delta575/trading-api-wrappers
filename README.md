# Trading API Wrappers
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Updates](https://pyup.io/repos/github/delta575/trading-api-wrappers/shield.svg)](https://pyup.io/repos/github/delta575/trading-api-wrappers/)
[![Python 3](https://pyup.io/repos/github/delta575/trading-api-wrappers/python-3-shield.svg)](https://pyup.io/repos/github/delta575/trading-api-wrappers/)

Trading API Wrappers.
Tested on Python 3.6

Supported APIs:

- [Bitfinex](https://www.bitfinex.com)
- [Bitstamp](https://www.bitstamp.net)
- [Buda](https://www.buda.com)
- [CoinDesk](https://www.coindesk.com)
- [CoinMarketCap](https://coinmarketcap.com)
- [CryptoMKT](https://www.cryptomkt.com)
- [Kraken](https://www.kraken.com)
- [OpenExchangeRates](https://openexchangerates.org)

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
