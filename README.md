# Trading API Wrappers

Trading API Wrappers.
Tested on Python 3.5

- [Bitfinex](https://www.bitfinex.com)
- [Kraken](http://www.kraken.com)
- [SURBTC](https://www.surbtc.com)
- [CoinDesk](http://www.coindesk.com)

## Dev setup

Install the libs

    pip install -r requirements.txt

Rename .env.example > .env

## Installation

    pip install git+https://github.com/delta575/trading-api-wrappers.git

## Usage

### Bitfinex

Public API:

    from trading_api_wrappers import Bitfinex
    client = Bitfinex.Public()

Authenticated API:

    from trading_api_wrappers import Bitfinex
    client = Bitfinex.Auth(API_KEY, API_SECRET)

Bitfinex API Doc:
https://bitfinex.readme.io/v1/docs

### Kraken

Public API:

    from trading_api_wrappers import Kraken
    client = Kraken.Public()

Authenticated API:

    from trading_api_wrappers import Kraken
    client = Kraken.Auth(API_KEY, API_SECRET)

Kraken API Doc:
https://www.kraken.com/help/api

### SURBTC

Public API:

    from trading_api_wrappers import SURBTC
    client = SURBTC.Public()

Authenticated API:

    from trading_api_wrappers import SURBTC
    client = SURBTC.Auth(API_KEY, API_SECRET)

SURBTC API Doc:
https://api.surbtc.com/

### CoinDesk

    from trading_api_wrappers import CoinDesk
    client = CoinDesk()    

Coindesk API Doc:
http://www.coindesk.com/api

### CryptoMKT

    from trading_api_wrappers import CryptoMKT
    client = CryptoMKT()    

*No API Docs for CryptoMKT!*

## Licence

Copyright (c) 2017 Felipe Aránguiz | Sebastián Aránguiz

See [LICENSE](LICENSE)

## Based on

[scottjbarr/bitfinex](https://github.com/scottjbarr/bitfinex)
