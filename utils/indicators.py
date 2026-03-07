# utils/indicators.py
import pandas as pd

def sma(series: pd.Series, period: int) -> pd.Series:
    """
    Простая скользящая средняя.
    :param series: pandas Series цен закрытия
    :param period: период SMA
    :return: pandas Series с SMA
    """
    return series.rolling(window=period).mean()


def is_bullish_pinbar(open_price, high, low, close) -> bool:
    """
    Проверка, является ли свеча Bullish PinBar
    :return: True если свеча бычья PinBar
    """
    body = abs(close - open_price)
    lower_wick = min(open_price, close) - low
    upper_wick = high - max(open_price, close)

    # Условия PinBar
    if body == 0:
        return False  # избегаем деления на ноль
    return lower_wick / body > 2 and body < (high - low) * 0.3


def is_bearish_pinbar(open_price, high, low, close) -> bool:
    """
    Проверка, является ли свеча Bearish PinBar
    :return: True если свеча медвежья PinBar
    """
    body = abs(close - open_price)
    lower_wick = min(open_price, close) - low
    upper_wick = high - max(open_price, close)

    if body == 0:
        return False
    return upper_wick / body > 2 and body < (high - low) * 0.3