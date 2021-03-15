from pycoingecko import CoinGeckoAPI
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
import time
import csv

# usd pairs from GDAX, Kraken 
# + some extras
filter = ['btc', 'eth', 'ltc', 'bch', 'eos', 'dash', 'oxt', 'mkr', 'xlm', 'atom', 'xtz', 'etc', 'omg', 'zec', 'link', 'rep', 'zrx', 'algo', 'dai', 'knc', 'comp', 'band', 'nmr', 'uma', 'lrc', 'yfi', 'uni', 'ren', 'bal', 'wbtc', 'nu', 'fil', 'aave', 'grt', 'bnt', 'snx',
          'ant', 'bat', 'ada', 'crv', 'mana', 'doge', 'ewt', 'flow', 'gno', 'icx', 'kava', 'keep', 'ksm', 'lsk', 'xmr', 'nano', 'ocean', 'paxg', 'dot', 'qtum', 'xrp', 'sc', 'storj', 'trx', 'waves',
          'req']


csv_fields = ['ticker', 'mcap vel', 'mcap acc']
csv_data = []

cg = CoinGeckoAPI()

marketCaps = cg.get_coins_markets(vs_currency='usd', order="market_cap_desc", per_page=250, page=1)
marketCaps += cg.get_coins_markets(vs_currency='usd', order="market_cap_desc", per_page=250, page=2)
marketCapsJson = (json.dumps(marketCaps, indent=4, sort_keys=True))
with open('MarketCaps.json', 'w') as f:
    json.dump(marketCaps, f)
    
marketCapDF = pd.read_json('MarketCaps.json')

# Data-structs
avgVelPerID = {} #avg mcap vel per increment
avgAccelPerID = {} #avg mcap vel per increment

#temporary to limit amount of plots to add.
curIndex = 0
numQueries = 0

#go through each symbol
for ticker in filter:
    found = True
    try:
        curIndex = marketCapDF["symbol"][marketCapDF["symbol"] == ticker].index[0]
    except:
        print('could not find ticker ' + ticker)
        found = False
    if  found:
        #print('found ticker ' + ticker + " index = " + str(curIndex))
        numQueries += 1
        if numQueries > 0 and numQueries % 2 == 0:
                time.sleep(1.05) # so we don't get denied from too many queries
        
        #get market chart which returns prices,market_caps & total_volumes.
        market_chart = cg.get_coin_market_chart_by_id(id=marketCapDF["id"][curIndex], vs_currency='usd', days=30)
    
        avgVel = []
        avgAccel = []
        avgAccel.append(0.00)

        #collect
        i = 1
        while i < len(market_chart["market_caps"]):
            #need to divide by 1000 for some reason. Found a stack overflow solution.
            #scatterData["data"][0]["x"].append(datetime.fromtimestamp(entry[0] / 1000))
            #scatterData["data"][0]["y"].append(entry[1])
            avgVel.append(market_chart["market_caps"][i][1] - market_chart["market_caps"][i-1][1])
            if i > 1:
                avgAccel.append(avgVel[i-1] - avgVel[i-2])
            i += 1                
                           
        csv_data.append([ticker, avgVel[-1], avgAccel[-1]]);
        avgVelPerID[marketCapDF["symbol"][curIndex]] = avgVel
        avgAccelPerID[marketCapDF["symbol"][curIndex]] = avgAccel

with open('mcap_data.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, lineterminator = '\n')
		writer.writerow(csv_fields)
		writer.writerows(csv_data)

print('done')