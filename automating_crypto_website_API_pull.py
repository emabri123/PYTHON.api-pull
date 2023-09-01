from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import os
import time
import seaborn as sns
import matplotlib.pyplot as plt

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '60189122-57d6-4e1c-85d5-c387a9474176',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  #print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

df = pd.json_normalize(data['data'])
#pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
df['timestamp'] = pd.to_datetime('now')

print(df)

df3 = df.groupby('name', sort = 'False')[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean()
df4 = df3.stack()
df5 = df4.to_frame(name='values')
df6 = df5.reset_index()
df7 = df6.rename(columns={'level_1':'percent_change'})
df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_90d','quote.USD.percent_change_60d','quote.USD.percent_change_30d','quote.USD.percent_change_7d','quote.USD.percent_change_24h','quote.USD.percent_change_1h'],['90d','60d','30d','7d','24h','1h'])

print(df7)

sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')
plt.show()

def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'15',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '60189122-57d6-4e1c-85d5-c387a9474176',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    df = pd.json_normalize(data['data'])
    df['timestamp'] = pd.to_datetime('now')
    df

    if not os.path.isfile(r'C:\Users\Ema\Desktop\alex\_PORTFOLIO\PYTHON_API_PULL\API.csv'):
       df.to_csv(r'C:\Users\Ema\Desktop\alex\_PORTFOLIO\PYTHON_API_PULL\API.csv', header='column_names')
    else:
       df.to_csv(r'C:\Users\Ema\Desktop\alex\_PORTFOLIO\PYTHON_API_PULL\API.csv', mode='a', header=False)

for i in range(333):
   api_runner()
   print("API Runner completed!")
   time.sleep(60)
exit()





