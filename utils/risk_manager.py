def calculate_sl_tp(entry, pinbar_low, pinbar_high, side, rr=2, sl_offset_percent=0.02):
    """
    Рассчет Stop Loss и Take Profit
    :param entry: цена входа
    :param pinbar_low: low PinBar
    :param pinbar_high: high PinBar
    :param side: "LONG" или "SHORT"
    :param rr: Risk/Reward
    :param sl_offset_percent: смещение SL
    :return: sl, tp
    """
    if side == "LONG":
        sl_base = pinbar_low
        sl_size = entry - sl_base
        offset = sl_size * sl_offset_percent
        sl = sl_base - offset
        tp = entry + sl_size * rr
    elif side == "SHORT":
        sl_base = pinbar_high
        sl_size = sl_base - entry
        offset = sl_size * sl_offset_percent
        sl = sl_base + offset
        tp = entry - sl_size * rr
    else:
        raise ValueError("Side должен быть 'LONG' или 'SHORT'")
    return sl, tp

def calculate_position_size(deposit, risk_percent, entry, sl, side):
    """
    Рассчет размера позиции
    :param deposit: общий депозит
    :param risk_percent: процент риска на сделку
    :param entry: цена входа
    :param sl: стоп-лосс
    :param side: "LONG" или "SHORT"
    :return: размер позиции
    """
    risk_amount = deposit * risk_percent
    if side == "LONG":
        sl_size = entry - sl
    elif side == "SHORT":
        sl_size = sl - entry
    else:
        raise ValueError("Side должен быть 'LONG' или 'SHORT'")
    if sl_size == 0:
        return 0
    size = risk_amount / sl_size
    return size