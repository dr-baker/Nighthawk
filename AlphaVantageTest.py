from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time
import matplotlib.pyplot as plt

api_key = 'S3NUOGN1S4TKJF3W'

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='TSLA', interval = '60min', outputsize='full')
subset = data['1. open']
print(data)

# Want 5/20 to 6/5
# print(subset['2020-06-15 16:00:00':'2020-06-15 15:56:00'])
# data['4. close'].plot()
# plt.title('Intraday Times Series for the MSFT stock (1 min)')
# plt.show()


# print("two")
# print(subset['2020-06-15 15:59:00'])

# print(subset)
# for col in subset.columns: 
#     print(col) 