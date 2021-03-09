from pycoingecko import CoinGeckoAPI
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta

cg = CoinGeckoAPI()

marketCaps = cg.get_coins_markets(vs_currency='usd', order="market_cap_desc", per_page="200")
marketCapsJson = (json.dumps(marketCaps, indent=4, sort_keys=True))
with open('MarketCaps.json', 'w') as f:
    json.dump(marketCaps, f)
    
marketCapDF = pd.read_json('MarketCaps.json')

# Data-structs
avgVelPerID = {} #avg mcap vel per increment
avgAccelPerID = {} #avg mcap vel per increment

#temporary to limit amount of plots to add.
curIndex = 0
maxCount = 2

#go through each symbol
while curIndex < len(marketCapDF["id"]):
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

    avgVelPerID[marketCapDF["symbol"][curIndex]] = avgVel
    avgAccelPerID[marketCapDF["symbol"][curIndex]] = avgAccel

   
    if curIndex == maxCount:
        break
    curIndex +=1