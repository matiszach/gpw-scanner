import lib.scraper as scraper
from datetime import date, timedelta
import numpy as np

def x_days_ago(days):
    return (date.today() - timedelta(days=days)).strftime('%d-%m-%Y')


def get_tickers(date_point=date.today()):
    df, tickers = [], []
    while len(tickers) == 0:
        df, tickers = scraper.get_data(date_point)
        date_point -= timedelta(days=1)

    return [ticker for ticker in tickers if type(df['open'][ticker]) == np.float64]


def get_2weeks_tickers():
    curr = get_tickers()
    pre = get_tickers(date.today() - timedelta(days=7))
    return [ticker for ticker in curr if ticker in pre]


def periodic_candle(end_day, no_days):
    ans = []
    tickers = []
    last_tickers = []
    for day in range(no_days):
        df, tickers = scraper.get_data((end_day - timedelta(day)).strftime('%d-%m-%Y'))
        if len(tickers) == 0:
            continue

        if len(ans) == 0:
            ans = df[:]
        else:
            if len(last_tickers) != 0:
                tickers = [ticker for ticker in tickers if ticker in last_tickers and type(df['open'][ticker]) == np.float64]

            for ticker in tickers:
                ans.loc[ticker, 'close'] = df['close'][ticker]
                ans.loc[ticker, 'min'] = min(ans['min'][ticker], df['min'][ticker])
                ans.loc[ticker, 'max'] = max(ans['max'][ticker], df['max'][ticker])
                ans.loc[ticker, 'vol'] += df['vol'][ticker]
                ans.loc[ticker, 'stock_vol'] += df['stock_vol'][ticker]
                ans.loc[ticker, 'opers'] += df['opers'][ticker]

        last_tickers = tickers

    for ticker in tickers:
        ans.loc[ticker, 'change'] = (1 - ans['open'][ticker] / ans['close'][ticker]) * 100
    return ans


def this_friday(date_point):
    return date_point + timedelta(days=(4 - date_point.weekday()))
