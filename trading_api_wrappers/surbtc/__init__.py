import warnings

from trading_api_wrappers.buda import Buda, BudaAuth, BudaPublic

__all__ = [
    'SURBTC',
]

DEPRECATION_WARNING = (
    'SurBTC.com has changed to Buda.com, please use the `buda` package.',
    PendingDeprecationWarning
)


class SURBTCAuth(BudaAuth):
    def __init__(self, *args, **kwargs):
        warnings.warn(*DEPRECATION_WARNING)
        super(SURBTCAuth, self).__init__(*args, **kwargs)


class SURBTCPublic(BudaPublic):
    def __init__(self, *args, **kwargs):
        warnings.warn(*DEPRECATION_WARNING)
        super(SURBTCPublic, self).__init__(*args, **kwargs)


class SURBTC(Buda):
    Auth = SURBTCAuth
    Public = SURBTCPublic

    def __init__(self):
        warnings.warn(*DEPRECATION_WARNING)
