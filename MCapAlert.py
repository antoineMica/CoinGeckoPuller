from pycoingecko import CoinGeckoAPI
#import plotly.graph_objects as go
#import plotly.io as pio
#from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
import time
import csv

from twilio.rest import Client

account_sid = ''
auth_token = ''
from_tel = '+12223334444'
to_tel = '+12223334444'


with open('auth.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    account_sid = csv_reader.fieldnames[0]
    auth_token = csv_reader.fieldnames[1]
    from_tel = csv_reader.fieldnames[2]
    to_tel = csv_reader.fieldnames[3]

twilio_client = Client(account_sid, auth_token)

# usd pairs from GDAX, Kraken 
# + some extras
filter = ['btc', 'eth', 'ltc', 'bch', 'eos', 'dash', 'mkr', 'xlm', 'atom', 'xtz', 'etc', 'omg', 'zec', 'link', 'rep', 'zrx', 'algo', 'dai', 'knc', 'comp', 'band', 'nmr', 'uma', 'lrc', 'yfi', 'uni', 'ren', 'bal', 'wbtc', 'nu', 'fil', 'aave', 'grt', 'bnt', 'snx',
          'ant', 'bat', 'ada', 'crv', 'mana', 'doge', 'ewt', 'flow', 'gno', 'icx', 'kava', 'keep', 'ksm', 'lsk', 'xmr', 'nano', 'ocean', 'paxg', 'dot', 'qtum', 'xrp', 'sc', 'storj', 'trx', 'waves',
          'req']


csv_fields = ['ticker', 'mcap vel', 'mcap acc']
csv_data = []

cg = CoinGeckoAPI()

mcap_recent_snapshot = {}

#populate an initial mcap snapshot
markets_snapshot = cg.get_coins_markets(vs_currency='usd', order="market_cap_desc", per_page=250, page=1)
markets_snapshot += cg.get_coins_markets(vs_currency='usd', order="market_cap_desc", per_page=250, page=2)
for entry in markets_snapshot:
    mcap_recent_snapshot[entry['symbol']] = entry['market_cap_rank']

iteration = 0
while True:
    print(iteration)
    time.sleep(60)

    markets_snapshot = cg.get_coins_markets(vs_currency='usd', order="market_cap_desc", per_page=250, page=1)
    markets_snapshot += cg.get_coins_markets(vs_currency='usd', order="market_cap_desc", per_page=250, page=2)

    sms_alert_msg = ""

    for entry in markets_snapshot:
        try:
            if mcap_recent_snapshot[entry['symbol']] != entry['market_cap_rank']:
                    if entry['symbol'] in filter:
                        sms_alert_msg += '\n' + entry['symbol'] + ' ' + str(mcap_recent_snapshot[entry['symbol']]) + '->' + str(entry['market_cap_rank'])
        except KeyError:
            print (entry['symbol'])
        mcap_recent_snapshot[entry['symbol']] = entry['market_cap_rank']
    
    if sms_alert_msg != "":
        twilio_client.messages .create(
                body =  '!!!MCAP ALERT!!!\n' + sms_alert_msg,
                from_ = from_tel,
                to =    to_tel)
            
    iteration += 1
   
print('done')