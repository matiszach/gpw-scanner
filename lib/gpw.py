import lib.manipulation as manip
from datetime import date, timedelta

import pandas as pd


def init():
    curr = manip.periodic_candle(manip.this_friday(date.today()), 5)
    pre = manip.periodic_candle(manip.this_friday(date.today() - timedelta(7)), 5)
    tickers = manip.get_tickers(manip.this_friday(date.today()))
    return pre, curr, tickers


def filter_data(df, tickers, min_volume=300):
    return [ticker for ticker in tickers if df['vol'][ticker] >= min_volume]


def sort_by_volume(df, tickers):
    return sorted(tickers, key=lambda ticker: -df['vol'][ticker])


def get_inside_bars(pre, curr, tickers):
    inside_bars = []
    for ticker in tickers:
        if curr['min'][ticker] >= pre['min'][ticker] and curr['max'][ticker] <= pre['max'][ticker]:
            inside_bars.append(ticker)

    return inside_bars


def get_inside_bars_strategy(pre, curr, tickers):
    data = []
    for ticker in tickers:
        data.append([ticker, curr['max'][ticker], curr['min'][ticker],
                     str(round((1 - curr['min'][ticker] / curr['max'][ticker]) * 100, 2)) + '%'])

    df = pd.DataFrame(data, index=tickers, columns=['walor', 'wybicie', 'stoploss', 'ryzyko'])
    return df
