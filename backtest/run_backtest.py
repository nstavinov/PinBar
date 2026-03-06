import pandas as pd
from strategies.pinbar_strategy import PinBarStrategy
import config
import os

def load_data(symbol, timeframe, folder):
    filename = f"{folder}/{symbol}_{timeframe}.csv"
    if not os.path.exists(filename):
        print(f"Файл с историей {filename} не найден!")
        return None
    df = pd.read_csv(filename, parse_dates=['datetime'], index_col='datetime')
    if 'symbol' not in df.columns:
        df['symbol'] = symbol
    return df

def main():
    # Чтение списка инструментов
    with open(config.symbols_file, 'r') as f:
        symbols = [line.strip() for line in f if line.strip()]

    all_signals = []

    for symbol in symbols:
        df = load_data(symbol, config.timeframe, config.data_folder)
        if df is None:
            continue

        strategy = PinBarStrategy(df, config)
        signals = strategy.run()
        print(f"--- {symbol} --- {len(signals)} сигналов")
        for s in signals:
            print(s)
        all_signals.extend(signals)

    # Сохранение всех сигналов в CSV
    if all_signals:
        all_df = pd.DataFrame(all_signals)
        all_df.to_csv(f"{config.data_folder}/all_signals.csv", index=False)
        print(f"\nСигналы всех инструментов сохранены в {config.data_folder}/all_signals.csv")

if __name__ == "__main__":
    main()