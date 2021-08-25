from .bitcoinity import *  # noqa: F401
from .bitex import *  # noqa: F401
from .bitfinex import *  # noqa: F401
from .bitstamp import *  # noqa: F401
from .buda import *  # noqa: F401
from .coindesk import *  # noqa: F401
from .coinmarketcap import *  # noqa: F401
from .cryptomkt import *  # noqa: F401
from .currencylayer import *  # noqa: F401
from .errors import *  # noqa: F401
from .kraken import *  # noqa: F401
from .oxr import *  # noqa: F401
from .ripio import *  # noqa: F401
from .sfox import *  # noqa: F401
from .surbtc import *  # noqa: F401

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)
