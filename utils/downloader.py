# utils/downloader.py (incremental с data_start_date)

import ccxt
import os
import pandas as pd
from datetime import datetime
from config import data_folder, symbols_file, timeframe, data_start_date

os.makedirs(data_folder, exist_ok=True)
DEBUG = True

exchange = ccxt.binance({'options': {'defaultType': 'future'}})

def load_symbols(file_path=symbols_file, debug=DEBUG):
    with open(file_path, "r", encoding="utf-8") as f:
        symbols = [line.strip() for line in f if line.strip()]
    if debug:
        print(f"Загружено {len(symbols)} инструментов из {file_path}")
    return symbols

def fetch_ohlcv_iter(symbol, since=None, limit=500, debug=DEBUG):
    """Итеративно скачиваем OHLCV по пакетам"""
    all_data = []
    current_since = since
    while True:
        df = None
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe.lower(), since=current_since, limit=limit)
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        except Exception as e:
            if debug:
                print(f"Ошибка {symbol}: {e}")
            break

        if df is None or df.empty:
            break

        all_data.append(df)
        last_ts = df["timestamp"].max()
        if len(df) < limit:
            break  # дошли до последней свечи
        current_since = last_ts + 1  # следующий пакет

    if all_data:
        return pd.concat(all_data).drop_duplicates(subset="timestamp").reset_index(drop=True)
    return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

def save_ohlcv(symbol, df, debug=DEBUG):
    safe_symbol = symbol.replace("/", "")
    file_path = os.path.join(data_folder, f"{safe_symbol}_{timeframe}.csv")
    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path)
        combined = pd.concat([old_df, df]).drop_duplicates(subset="timestamp").reset_index(drop=True)
        combined.to_csv(file_path, index=False)
        if debug:
            print(f"Обновлено: {file_path} ({len(combined)} строк)")
    else:
        df.to_csv(file_path, index=False)
        if debug:
            print(f"Сохранено: {file_path} ({len(df)} строк)")

def download_all(debug=DEBUG):
    symbols = load_symbols(debug=debug)
    for symbol in symbols:
        safe_symbol = symbol.replace("/", "")
        file_path = os.path.join(data_folder, f"{safe_symbol}_{timeframe}.csv")
        if os.path.exists(file_path):
            old_df = pd.read_csv(file_path)
            since = int(old_df["timestamp"].max()) + 1
            if debug:
                print(f"{symbol}: скачиваем новые свечи с {since}")
        else:
            dt = datetime.strptime(data_start_date, "%Y-%m-%d")
            since = int(dt.timestamp() * 1000)
            if debug:
                print(f"{symbol}: файл не найден, начинаем с {data_start_date}")
        df = fetch_ohlcv_iter(symbol, since=since, debug=debug)
        if not df.empty:
            save_ohlcv(symbol, df, debug=debug)

if __name__ == "__main__":
    download_all()