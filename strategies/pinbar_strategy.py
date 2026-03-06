from utils.indicators import sma, is_bullish_pinbar, is_bearish_pinbar
from utils.risk_manager import calculate_sl_tp, calculate_position_size

class PinBarStrategy:
    """
    Реализация PinBar стратегии:
    - Фильтр тренда: SMA(config.sma_period)
    - Расчёт SL и TP с RR = 1:2 и offset
    - Поддержка LONG/SHORT по каждому инструменту отдельно
    """
    def __init__(self, df, config):
        self.df = df.copy()
        self.config = config
        # Вычисляем SMA
        self.df['SMA'] = sma(df['close'], config.sma_period)
        self.signals = []

    def run(self):
        """
        Основной метод стратегии.
        Проходим по каждой свече, ищем PinBar и создаем сигнал на следующую свечу.
        """
        for i in range(1, len(self.df)):
            row = self.df.iloc[i]
            prev = self.df.iloc[i-1]
            side = None

            # Проверяем PinBar на предыдущей свече
            if is_bullish_pinbar(prev['open'], prev['high'], prev['low'], prev['close']) and prev['close'] > prev['SMA']:
                side = "LONG"
            elif is_bearish_pinbar(prev['open'], prev['high'], prev['low'], prev['close']) and prev['close'] < prev['SMA']:
                side = "SHORT"

            if side:
                entry = row['open']
                sl, tp = calculate_sl_tp(
                    entry,
                    pinbar_low=prev['low'],
                    pinbar_high=prev['high'],
                    side=side,
                    rr=self.config.rr,
                    sl_offset_percent=self.config.sl_offset_percent
                )
                size = calculate_position_size(
                    deposit=self.config.deposit,
                    risk_percent=self.config.risk_percent,
                    entry=entry,
                    sl=sl,
                    side=side
                )
                self.signals.append({
                    'datetime': row.name,
                    'symbol': self.df.symbol.iloc[0] if 'symbol' in self.df.columns else 'UNKNOWN',
                    'side': side,
                    'entry': entry,
                    'sl': sl,
                    'tp': tp,
                    'size': size
                })
        return self.signals