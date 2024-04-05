import requests
import lxml
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


def get_data(date):
    page = requests.get('https://www.gpw.pl/archiwum-notowan-full?type=10&date=' + str(date))
    soup = BeautifulSoup(page.content, 'lxml')
    if page.text.find('Brak danych') != -1:
        return [], []

    tickers = [tmp.text.strip() for tmp in soup.find_all('td', class_='left')][::2]
    data = [tmp.text.replace(',', '.').strip().replace(' ', '')
            for tmp in soup.find_all('td', class_='text-right')]
    del data[0::9]

    data = np.array(data, dtype='float')
    data = np.array_split(data, len(tickers))
    df = pd.DataFrame(data, index=tickers,
                      columns=['open', 'max', 'min', 'close', 'change', 'stock_vol', 'opers', 'vol'])
    return df, tickers


