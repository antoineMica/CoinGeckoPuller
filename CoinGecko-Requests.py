from pycoingecko import CoinGeckoAPI
import json
cg = CoinGeckoAPI()

btcPrice = cg.get_coins_markets(vs_currency='usd', order="market_cap_desc", per_page="10")
#print(btcPrice)
print(json.dumps(btcPrice, indent=4, sort_keys=True))

btcPrice = cg.get_coins_markets(vs_currency='usd')