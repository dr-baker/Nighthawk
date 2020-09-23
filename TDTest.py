# Testing TDAmeritrade API
import requests
import pandas as pd
from datetime import datetime, timezone

ID = 'JWWOY8RNULF207ARHOBNGYHAEIGGMG0L'

mat = [['open', 'high', 'low', 'close', 'volume', 'time', 'time_readable', 'hour', 'minute']]
def listToMat(lst):
    for dict in lst:
        candle = list(dict.values());
        d = datetime.fromtimestamp(int(candle[5])/1000) # UTC time
#        d = d.strftime("%Y-%m-%d %H:%M:%S")
#        d = d.hour
        candle.append(d)
        candle.append(d.hour-7) # PDT hour
        candle.append(d.minute)
        mat.append(candle)


endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format('TSLA')
endDate = '1591340400000'; # 6/5

startDate = '1589958000000'; #5/20
#startDate = '1559718000000'; #6/5/19
#endDate = '1562310000000' #7/5/19
#startDate = 1557039600000;
#endDate = 1559718000000;
payload = {
    'apikey':ID,
    'frequencyType':'minute',
    'frequency':'1',
    'endDate':endDate,
    'startDate':startDate,
    'needExtendedHoursData':'true'}

content = requests.get(url=endpoint, params=payload)
data = content.json()
#print(type(data['candles'])) # list
#print(type(data['candles'][1])) # dict
listToMat(data['candles'])
df = pd.DataFrame(mat[1:], columns=mat[0])
print(df)
df.to_csv('t.csv', index=False)
df2 = df.loc[(df['hour'] == 6) & (df['minute'] >= 30) & (df['minute'] < 45)]
#df2 = np.where(a[:,'time_readable'].hour==6)
pd.set_option('display.max_rows', df.shape[0]+1)
print(df2)
#print(data)
