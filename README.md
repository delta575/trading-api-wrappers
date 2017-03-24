# Trading API Wrappers

Trading API Wrappers.
Tested on Python 3.5

- [Bitfinex](https://www.bitfinex.com)
- [SURBTC](https://www.surbtc.com)
- [CoinDesk](http://www.coindesk.com)
- [BtcVol](https://btcvol.info)

## Dev setup

Install the libs

    pip install -r requirements.txt

Rename .env.example > .env

## Installation

    pip install git+https://github.com/delta575/trading-api-wrappers.git

## Usage

### Bitfinex

Public API:

    from bitfinex import BitfinexPublic
    client = BitfinexPublic()

Authenticated API:

    from bitfinex import BitfinexAuth
    client = BitfinexAuth(API_KEY, API_SECRET)

Bitfinex API Doc:
https://bitfinex.readme.io/v1/docs

### SURBTC

    from surbtc import SURBTC
    client = SURBTC(API_KEY, API_SECRET)

SURBTC API Doc:
https://www.surbtc.com/docs/api

### CoinDesk

    from coindesk import CoinDesk
    client = CoinDesk()    

Coindesk API Doc:
http://www.coindesk.com/api

### BtcVol

    from btcvol import BtcVol
    client = BtcVol()

BtcVol API Doc:
https://btcvol.info

## Licence

Copyright (c) 2016 Felipe Aránguiz | Sebastián Aránguiz

See [LICENSE](LICENSE)

## Based on

[scottjbarr/bitfinex](https://github.com/scottjbarr/bitfinex)
