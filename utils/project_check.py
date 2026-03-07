import os
import pandas as pd

from config import symbols_file, data_folder, timeframe
from utils.symbols import normalize_symbol, to_filename


REQUIRED_COLUMNS = [
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume"
]


def check_symbols_file():
    if not os.path.exists(symbols_file):
        print(f"❌ Файл {symbols_file} не найден")
        return []

    with open(symbols_file, "r") as f:
        symbols = [normalize_symbol(line.strip()) for line in f if line.strip()]

    print(f"✅ symbols file OK ({len(symbols)} symbols)")
    return symbols


def check_data_folder():
    if not os.path.exists(data_folder):
        print(f"❌ Папка {data_folder} не найдена")
        return False

    print(f"✅ data folder OK ({data_folder})")
    return True


def check_csv(symbol):
    filename = to_filename(symbol, timeframe)
    path = os.path.join(data_folder, filename)

    if not os.path.exists(path):
        print(f"❌ нет файла: {filename}")
        return False

    try:
        df = pd.read_csv(path)

        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                print(f"❌ {filename} нет колонки {col}")
                return False

        print(f"✅ {filename} OK ({len(df)} rows)")
        return True

    except Exception as e:
        print(f"❌ ошибка чтения {filename}: {e}")
        return False


def run_project_check():
    print("\n=== PROJECT CHECK ===\n")

    if not check_data_folder():
        return False

    symbols = check_symbols_file()

    if not symbols:
        return False

    ok_count = 0

    for symbol in symbols:
        if check_csv(symbol):
            ok_count += 1

    print("\n=== RESULT ===")

    print(f"CSV OK: {ok_count}/{len(symbols)}")

    if ok_count == len(symbols):
        print("✅ PROJECT READY")
        return True
    else:
        print("⚠ PROJECT HAS ERRORS")
        return False