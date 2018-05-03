Trading API Wrappers
====================

|License: MIT| |Updates| |Python 3|

Trading API Wrappers. Tested on Python 3.6

Supported APIs:

-  `Bitfinex <https://www.bitfinex.com>`__
-  `Bitstamp <https://www.bitstamp.net>`__
-  `Buda <https://www.buda.com>`__
-  `CoinDesk <https://www.coindesk.com>`__
-  `CoinMarketCap <https://coinmarketcap.com>`__
-  `CryptoMKT <https://www.cryptomkt.com>`__
-  `Kraken <https://www.kraken.com>`__
-  `OpenExchangeRates <https://openexchangerates.org>`__

Dev setup
---------

Install the libs

.. code:: bash

    $ pip install -r requirements.txt

Rename ``.env.example`` to ``.env``

Installation
------------

.. code:: bash

    $ pip install git+https://github.com/delta575/trading-api-wrappers.git

Usage
-----

Bitfinex
~~~~~~~~

Public API:

.. code:: python

    from trading_api_wrappers import Bitfinex
    client = Bitfinex.Public()

Authenticated API:

.. code:: python

    from trading_api_wrappers import Bitfinex
    client = Bitfinex.Auth(API_KEY, API_SECRET)

Bitfinex API Doc: https://bitfinex.readme.io/v1/docs

Bitstamp
~~~~~~~~

Public API:

.. code:: python

    from trading_api_wrappers import Bitstamp
    client = Bitstamp.Public()

Authenticated API:

.. code:: python

    from trading_api_wrappers import Bitstamp
    client = Bitstamp.Auth(API_KEY, API_SECRET, CUSTOMER_ID)

Bitstamp API Doc: https://www.bitstamp.net/api

Buda
~~~~

Public API:

.. code:: python

    from trading_api_wrappers import Buda
    client = Buda.Public()

Authenticated API:

.. code:: python

    from trading_api_wrappers import Buda
    client = Buda.Auth(API_KEY, API_SECRET)

Buda API Doc: https://api.buda.com

Kraken
~~~~~~

Public API:

.. code:: python

    from trading_api_wrappers import Kraken
    client = Kraken.Public()

Authenticated API:

.. code:: python

    from trading_api_wrappers import Kraken
    client = Kraken.Auth(API_KEY, API_SECRET)

Kraken API Doc: https://www.kraken.com/help/api

CoinDesk
~~~~~~~~

.. code:: python

    from trading_api_wrappers import CoinDesk
    client = CoinDesk()

CoinDesk API Doc: https://www.coindesk.com/api

CoinMarketCap
~~~~~~~~~~~~~

.. code:: python

    from trading_api_wrappers import CoinMarketCap
    client = CoinMarketCap()

CoinMarketCap API Doc: https://coinmarketcap.com/api

CryptoMKT
~~~~~~~~~

Public API:

.. code:: python

    from trading_api_wrappers import CryptoMKT
    client = CryptoMKT.Public()

Authenticated API:

.. code:: python

    from trading_api_wrappers import CryptoMKT
    client = CryptoMKT.Auth(API_KEY, API_SECRET)

CryptoMKT API Doc: https://developers.cryptomkt.com

OpenExchangeRates
~~~~~~~~~~~~~~~~~

.. code:: python

    from trading_api_wrappers import OXR
    client = OXR(APP_ID)

OpenExchangeRates API Doc: https://docs.openexchangerates.org

CurrencyLayer
~~~~~~~~~~~~~

.. code:: python

    from trading_api_wrappers import CurrencyLayer
    client = CurrencyLayer(ACCESS_KEY)

CurrencyLayer API Doc: https://currencylayer.com/documentation

Licence
-------

|License: MIT|

The MIT License

Copyright © 2017 `Felipe Aránguiz <mailto://faranguiz575@gmail.com>`__
\| `Sebastián Aránguiz <mailto://sarang575@gmail.com>`__

See `LICENSE <LICENSE>`__

Donations
---------

Bitcoin:

::

    186kDw9LFcPvup17YSrWZbFqdZzELUFad3

Ether:

::

    0xeF38fA6c0a37A1BdB60CADd7f6e71F351F6d2583

.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
.. |Updates| image:: https://pyup.io/repos/github/delta575/trading-api-wrappers/shield.svg
   :target: https://pyup.io/repos/github/delta575/trading-api-wrappers/
.. |Python 3| image:: https://pyup.io/repos/github/delta575/trading-api-wrappers/python-3-shield.svg
   :target: https://pyup.io/repos/github/delta575/trading-api-wrappers/
