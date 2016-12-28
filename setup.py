from setuptools import setup

setup(
    name='trading_api_wrappers',
    version='0.1.0',
    description='Trading API Wrappers for Python 3',
    url='https://github.com/delta575/trading-api-wrappers',
    author='Felipe Aránguiz, Sebastián Aránguiz',
    authoremail='faranguiz575@gmail.com, sarang575@gmail.com',
    license='MIT',
    packages=[
        'trading_api_wrappers',
        'trading_api_wrappers.bitfinex',
        'trading_api_wrappers.btcvol',
        'trading_api_wrappers.coindesk',
        'trading_api_wrappers.surbtc',
    ],
    package_dir={
        'trading_api_wrappers': 'trading_api_wrappers',
    },
    install_requires=[
        'requests',
    ],
    tests_require=[
        'coverage>=4.2',
        'python-decouple>=3.0',
    ],
    zip_safe=True
)
