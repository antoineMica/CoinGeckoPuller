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

today = datetime.now()    
fromTS = datetime.timestamp(today - timedelta(days=10))
fig = make_subplots()

marketCapListByID = []

#temporary to limit amount of plots to add.
count = 1
maxCount = 2
#go through each symbol
for symb in marketCapDF["id"]:
    #get market chart which returns prices,market_caps & total_volumes.
    market_chart = cg.get_coin_market_chart_by_id(id=symb, vs_currency='usd', days=10)
    #gather plot data for current symbol
    scatterData = {
      "data" :  [{"type": "scatter",
              "x": [],
              "y": []}]
    }

    #collect
    for entry in market_chart["market_caps"]:
        #need to divide by 1000 for some reason. Found a stack overflow solution.
        scatterData["data"][0]["x"].append(datetime.fromtimestamp(entry[0] / 1000))
        scatterData["data"][0]["y"].append(entry[1])

    fig.add_trace(go.Scatter(x=scatterData["data"][0]["x"], y=scatterData["data"][0]["y"], name=symb))
    if count == maxCount:
        break
    count +=1
fig.show()