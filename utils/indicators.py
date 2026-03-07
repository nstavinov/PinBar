import pandas as pd

def sma(series, period):
    """
    Простая скользящая средняя
    :param series: pd.Series с ценами закрытия
    :param period: период SMA
    :return: pd.Series с SMA
    """
    return series.rolling(period).mean()

def is_bullish_pinbar(open_, high, low, close):
    """
    Проверка на бычий PinBar
    - маленькое тело
    - длинная нижняя тень > 2 * тело
    """
    body = abs(close - open_)
    lower_wick = min(open_, close) - low
    if body == 0:
        return False
    return lower_wick / body > 2

def is_bearish_pinbar(open_, high, low, close):
    """
    Проверка на медвежий PinBar
    - маленькое тело
    - длинная верхняя тень > 2 * тело
    """
    body = abs(close - open_)
    upper_wick = high - max(open_, close)
    if body == 0:
        return False
    return upper_wick / body > 2