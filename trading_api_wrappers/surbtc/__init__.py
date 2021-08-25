import warnings

from trading_api_wrappers.buda import Buda, BudaAuth, BudaPublic

__all__ = [
    "SURBTC",
]

deprecation_warning = (
    "SurBTC.com has changed to Buda.com, please use the `buda` package.",
    PendingDeprecationWarning,
)


class SURBTCAuth(BudaAuth):
    def __init__(self, *args, **kwargs):
        warnings.warn(*deprecation_warning)
        super(SURBTCAuth, self).__init__(*args, **kwargs)


class SURBTCPublic(BudaPublic):
    def __init__(self, *args, **kwargs):
        warnings.warn(*deprecation_warning)
        super(SURBTCPublic, self).__init__(*args, **kwargs)


class SURBTC(Buda):
    Auth = SURBTCAuth
    Public = SURBTCPublic

    def __init__(self):
        warnings.warn(*deprecation_warning)
