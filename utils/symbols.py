"""
Утилиты для работы с торговыми символами.

Внутренний стандарт проекта:
BTCUSDT
ETHUSDT
XRPUSDT
"""

def normalize_symbol(symbol: str) -> str:
    """
    Приводит любой формат символа к внутреннему стандарту.
    
    BTC/USDT -> BTCUSDT
    BTC_USDT -> BTCUSDT
    btcusdt  -> BTCUSDT
    """
    symbol = symbol.upper()
    symbol = symbol.replace("/", "")
    symbol = symbol.replace("_", "")
    return symbol


def to_ccxt(symbol: str) -> str:
    """
    Формат для ccxt / биржевых API.

    BTCUSDT -> BTC/USDT
    """
    symbol = normalize_symbol(symbol)
    base = symbol[:-4]
    quote = symbol[-4:]
    return f"{base}/{quote}"


def from_ccxt(symbol: str) -> str:
    """
    Формат из ccxt -> внутренний.
    
    BTC/USDT -> BTCUSDT
    """
    return normalize_symbol(symbol)


def to_filename(symbol: str, timeframe: str) -> str:
    """
    Имя файла с OHLCV.

    BTCUSDT + 4H -> BTCUSDT_4H.csv
    """
    symbol = normalize_symbol(symbol)
    return f"{symbol}_{timeframe}.csv"


def split_symbol(symbol: str):
    """
    Разделяет символ на base и quote.

    BTCUSDT -> ('BTC', 'USDT')
    """
    symbol = normalize_symbol(symbol)
    base = symbol[:-4]
    quote = symbol[-4:]
    return base, quote