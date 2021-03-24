from pycoingecko import CoinGeckoAPI
import csv
import time

cg = CoinGeckoAPI()

filter = []
with open('filter.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for entry in csv_reader.fieldnames:
        filter.append(entry)

id_map = {}

markets_snapshot = cg.get_coins_markets(vs_currency='usd', order="market_cap_desc", per_page=250, page=1)
markets_snapshot += cg.get_coins_markets(vs_currency='usd', order="market_cap_desc", per_page=250, page=2)
for entry in markets_snapshot:
    if entry['symbol'] in filter:
        id_map[entry['symbol']] = entry['id']


#go through each symbol
with open('mcap_hist.csv', mode='w', newline='') as csv_file:

    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for symb in filter:
        coin_hist = cg.get_coin_market_chart_by_id(id=id_map[symb], vs_currency='usd', days=30)

        row = [symb]
        for entry in coin_hist["market_caps"]:
            row.append(entry[1])
            
        writer.writerow(row)
        time.sleep(1)
