from datetime import date, timedelta
import lib.scraper as scraper
import lib.manipulation as manip
import lib.gpw as gpw
import lib.notifications as mailing
import math
from dotenv import load_dotenv
import os


load_dotenv()

min_volume = int(os.getenv("MIN_VOLUME"))

pre, curr, tickers = gpw.init()

tickers = gpw.filter_data(curr, tickers, min_volume)
tickers = gpw.sort_by_volume(curr, tickers)
tickers = gpw.get_inside_bars(pre, curr, tickers)

df = gpw.get_inside_bars_strategy(pre, curr, tickers)
files = mailing.make_table(df)

if os.getenv("SEND") == 'Yes':
    content = ("W tym tygodniu inside bar wystąpił na " + str(len(tickers))
               + " spółkach z obrotem co najmniej " + str(min_volume) + "k PLN.")

    mailing.send_mail(mailing.make_title('Wybicia tygodnia '), content, files, os.getenv('SENDER'),
                      os.getenv('RECIPIENT'), os.getenv('PASSWORD'))
