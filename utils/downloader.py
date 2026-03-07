# utils/downloader.py

import ccxt
import os
import pandas as pd
from config import data_folder, symbols_file, timeframe  # параметры из config.py

# Папка для сохранения данных
os.makedirs(data_folder, exist_ok=True)

# Флаг дебага
DEBUG = True  # True — вывод в консоль, False — тихий режим

# Инициализация Binance USD-M Futures через ccxt
exchange = ccxt.binance({
    'options': {'defaultType': 'future'}
})

def load_symbols(file_path=symbols_file, debug=DEBUG):
    """Считываем список инструментов из файла"""
    with open(file_path, "r", encoding="utf-8") as f:
        symbols = [line.strip() for line in f if line.strip()]
    if debug:
        print(f"Загружено {len(symbols)} инструментов из {file_path}")
    return symbols

def fetch_ohlcv(symbol, debug=DEBUG):
    """Загружаем OHLCV с Binance"""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe.lower(), limit=500)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        if debug:
            print(f"Загружено {len(df)} свечей для {symbol}")
        return df
    except Exception as e:
        if debug:
            print(f"Ошибка при загрузке {symbol}: {e}")
        return None

def save_ohlcv(symbol, df, debug=DEBUG):
    """Сохраняем данные в CSV, корректируем имя для Windows"""
    safe_symbol = symbol.replace("/", "_")  # заменяем / на _
    file_path = os.path.join(data_folder, f"{safe_symbol}_{timeframe}.csv")
    df.to_csv(file_path, index=False)
    if debug:
        print(f"Сохранено: {file_path} ({len(df)} строк)")

def download_all(debug=DEBUG):
    """Загружаем OHLCV для всех символов из trading_symbols.txt"""
    symbols = load_symbols(debug=debug)
    if debug:
        print(f"Загружаем OHLCV для {len(symbols)} инструментов...")
    for symbol in symbols:
        df = fetch_ohlcv(symbol, debug=debug)
        if df is not None and not df.empty:
            save_ohlcv(symbol, df, debug=debug)

if __name__ == "__main__":
    download_all()