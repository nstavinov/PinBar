# backtest/run_backtest.py
import os
import pandas as pd
from strategies.pinbar_strategy import PinBarStrategy
from config import data_folder, symbols_file, timeframe, debug  # <-- берем debug из config

def load_ohlcv(symbol_file: str) -> pd.DataFrame:
    """
    Загружает OHLCV для символа из trading_symbols.txt
    Преобразует символы вида BTC/USDT -> BTCUSDT
    Файлы должны называться <SYMBOL>_<TIMEFRAME>.csv
    """
    symbol = symbol_file.replace("/", "")
    file_path = os.path.join(data_folder, f"{symbol}_{timeframe}.csv")

    if not os.path.exists(file_path):
        if debug:
            print(f"Файл с историей {file_path} не найден!")
        return None

    df = pd.read_csv(file_path)
    if debug:
        print(f"Загружено {len(df)} свечей для {symbol_file} ({file_path})")
    return df

def main():
    if not os.path.exists(symbols_file):
        print(f"Файл {symbols_file} не найден!")
        return

    with open(symbols_file, "r") as f:
        symbols = [line.strip() for line in f if line.strip()]

    if debug:
        print(f"Всего инструментов в {symbols_file}: {len(symbols)}")

    for symbol_file in symbols:
        df = load_ohlcv(symbol_file)
        if df is None:
            continue

        # Запуск стратегии PinBar
        strategy = PinBarStrategy(symbol_file, df)
        strategy.run_backtest()

if __name__ == "__main__":
    main()