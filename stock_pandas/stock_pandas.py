# This program is to retrieve stock price

import pandas
import pandas.io.data as web
from datetime import datetime

tickers = ['2800.HK', '0005.HK', '0011.HK', '0001.HK']

start = datetime(2014,1,1)
end = datetime(2014,12,31)
stockRawData = web.DataReader(tickers, 'yahoo', start, end)
print stockRawData

