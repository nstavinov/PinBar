# utils/get_perpetual_futures.py

import ccxt
import os

OUTPUT_FILE = "trading_symbols.txt"

# Создаём папку, если нужно
os.makedirs(os.path.dirname(OUTPUT_FILE) or ".", exist_ok=True)

# Инициализация Binance USD-M Futures через ccxt
exchange = ccxt.binance({
    'options': {'defaultType': 'future'}
})

def get_perpetual_usdt_usdc_futures(debug=True):
    """
    Получает список всех Perpetual Futures USDT/USDC
    Фильтрует только контракты с ':' в имени (маркер USD-M Futures)
    Чистит символы от ':USDT' / ':USDC'
    """
    markets = exchange.load_markets()
    perp_symbols = []

    for symbol in markets.keys():
        # Проверка: символ содержит ':' и оканчивается на :USDT или :USDC
        if (':' in symbol) and (symbol.endswith(':USDT') or symbol.endswith(':USDC')):
            clean_symbol = symbol.split(":")[0]  # убираем :USDT / :USDC
            perp_symbols.append(clean_symbol)
            if debug:
                print(f"  -> Добавлен: {clean_symbol} (оригинал: {symbol})")
        else:
            if debug:
                print(f"Пропущен (не фьючерс): {symbol}")

    if debug:
        print(f"\nВсего символов в markets: {len(markets)}")
        print(f"Выбрано Perpetual USDT/USDC: {len(perp_symbols)}")

        # Отдельно выводим USDT и USDC
        usdt_pairs = [s for s in perp_symbols if s.endswith('USDT')]
        usdc_pairs = [s for s in perp_symbols if s.endswith('USDC')]
        print(f"USDT-пары ({len(usdt_pairs)}): {usdt_pairs[:10]} ...")
        print(f"USDC-пары ({len(usdc_pairs)}): {usdc_pairs[:10]} ...")

    return perp_symbols

def save_symbols(symbols, file_path=OUTPUT_FILE):
    """Сохраняет список символов в файл с кодировкой UTF-8"""
    with open(file_path, "w", encoding="utf-8") as f:
        for symbol in symbols:
            f.write(symbol + "\n")
    print(f"\nСписок Perpetual USDT/USDC Futures сохранён в {file_path} ({len(symbols)} инструментов)")

if __name__ == "__main__":
    symbols = get_perpetual_usdt_usdc_futures(debug=False)
    save_symbols(symbols)