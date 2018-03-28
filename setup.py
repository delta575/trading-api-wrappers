import sys
from setuptools import setup

if not (sys.version_info >= (3, 6)):
    sys.exit('Only Python 3.6 or later is supported')

setup(
    name='trading_api_wrappers',
    version='0.6.1',
    description='Trading API Wrappers for Python 3.6',
    url='https://github.com/delta575/trading-api-wrappers',
    author='Felipe Aránguiz, Sebastián Aránguiz',
    authoremail='faranguiz575@gmail.com, sarang575@gmail.com',
    license='MIT',
    packages=[
        'trading_api_wrappers',
        'trading_api_wrappers.bitcoinity',
        'trading_api_wrappers.bitfinex',
        'trading_api_wrappers.bitstamp',
        'trading_api_wrappers.buda',
        'trading_api_wrappers.coindesk',
        'trading_api_wrappers.coinmarketcap',
        'trading_api_wrappers.cryptomkt',
        'trading_api_wrappers.currencylayer',
        'trading_api_wrappers.kraken',
        'trading_api_wrappers.oxr',
        'trading_api_wrappers.surbtc',
    ],
    package_dir={
        'trading_api_wrappers': 'trading_api_wrappers',
    },
    install_requires=[
        'requests',
    ],
    tests_require=[
        'python-decouple',
    ],
    zip_safe=True
)
