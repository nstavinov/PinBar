# config.py
try:
    from config_local import api_key, api_secret
except ImportError:
    api_key = ""
    api_secret = ""

# Остальная конфигурация стратегии
deposit = 1000
risk_percent = 0.05
rr = 2
sma_period = 42
sl_offset_percent = 0.02
timeframe = "4H"

order_type = "market"
commission = 0.0004
slippage = 0.0
data_folder = "ohlcv_cache/"
symbols_file = "trading_symbols.txt"
data_start_date = "2026-01-01"