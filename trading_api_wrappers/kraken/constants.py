from ..base import _Enum


# Kraken supported symbols
class Symbol(_Enum):
    BCHUSD = "BCHUSD"
    DASHEUR = "DASHEUR"
    DASHUSD = "DASHUSD"
    DASHXBT = "DASHXBT"
    USDTZUSD = "USDTUSD"
    XETCXETH = "ETCETH"
    XETCXXBT = "ETCXBT"
    XETCZEUR = "ETCEUR"
    XETCZUSD = "ETCUSD"
    XETHXXBT = "ETHXBT"
    # XETHXXBT.d = 'ETHXBT.d'
    XETHZCAD = "ETHCAD"
    # XETHZCAD.d = 'ETHCAD.d'
    XETHZEUR = "ETHEUR"
    # XETHZEUR.d = 'ETHEUR.d'
    XETHZGBP = "ETHGBP"
    # XETHZGBP.d = 'ETHGBP.d'
    XETHZJPY = "ETHJPY"
    # XETHZJPY.d = 'ETHJPY.d'
    XETHZUSD = "ETHUSD"
    # XETHZUSD.d = 'ETHUSD.d'
    XICNXETH = "ICNETH"
    XICNXXBT = "ICNXBT"
    XLTCXXBT = "LTCXBT"
    XLTCZEUR = "LTCEUR"
    XLTCZUSD = "LTCUSD"
    XMLNXETH = "MLNETH"
    XMLNXXBT = "MLNXBT"
    XREPXETH = "REPETH"
    XREPXXBT = "REPXBT"
    XREPZEUR = "REPEUR"
    XREPZUSD = "REPUSD"
    XXBTZCAD = "XBTCAD"
    # XXBTZCAD.d = 'XBTCAD.d'
    XXBTZEUR = "XBTEUR"
    # XXBTZEUR.d = 'XBTEUR.d'
    XXBTZGBP = "XBTGBP"
    # XXBTZGBP.d = 'XBTGBP.d'
    XXBTZJPY = "XBTJPY"
    # XXBTZJPY.d = 'XBTJPY.d'
    XXBTZUSD = "XBTUSD"
    # XXBTZUSD.d = 'XBTUSD.d'
    XXDGXXBT = "XDGXBT"
    XXLMXXBT = "XLMXBT"
    XXLMZEUR = "XLMEUR"
    XXLMZUSD = "XLMUSD"
    XXMRXXBT = "XMRXBT"
    XXMRZEUR = "XMREUR"
    XXMRZUSD = "XMRUSD"
    XXRPXXBT = "XRPXBT"
    XZECXXBT = "ZECXBT"
    XZECZEUR = "ZECEUR"
    XZECZUSD = "ZECUSD"


# Kraken supported currencies
class Currency(_Enum):
    DASH = "DASH"
    KFEE = "FEE"
    USDT = "USDT"
    XDAO = "DAO"
    XETC = "ETC"
    XETH = "ETH"
    XICN = "ICN"
    XLTC = "LTC"
    XMLN = "MLN"
    XNMC = "NMC"
    XREP = "REP"
    XXBT = "XBT"
    XXDG = "XDG"
    XXLM = "XLM"
    XXMR = "XMR"
    XXRP = "XRP"
    XXVN = "XVN"
    XZEC = "ZEC"
    ZCAD = "CAD"
    ZEUR = "EUR"
    ZGBP = "GBP"
    ZJPY = "JPY"
    ZKRW = "KRW"
    ZUSD = "USD"
