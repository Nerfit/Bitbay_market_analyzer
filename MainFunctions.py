from BitbayApi import Bitbay_Api

api = Bitbay_Api()

res = api.get(item='/trading/ticker')
# res = api.get(item='/trading/stats/XLM-BTC')
# res = api.get(item='/trading/orderbook-limited/BTC-PLN/10')
# print(res['items'].keys())

markets_keys = res['items'].keys()
# PLN, Bitcoin and Etherum markets
pln_markets = [x for x in markets_keys if '-PLN' in x]
btc_markets = [x for x in markets_keys if '-BTC' in x]
eth_markets = [x for x in markets_keys if '-ETH' in x]
pln_btc_mutual = [x.split('-')[0] for x in pln_markets if x.split('-')[0] + '-BTC' in btc_markets]
pln_eth_mutual = [x.split('-')[0] for x in pln_markets if x.split('-')[0] + '-ETH' in eth_markets]

print(res['items']['XLM-BTC']['highestBid'])

# Crypto-crypto fee: 0.1%
crypto_crypto_fee = 0.001
# Crypto-FIAT fee (worst scenario): 0.38%
crypto_fiat_fee = 0.0038
# Money to spend
moneyPLN = 15000

def get_best_markets(all_mutual_markets):
    affordable_markets = []
    for market in all_mutual_markets:
        lowest_ask = res['items'][market + '-BTC']['lowestAsk']
        # market_cash = lowest_ask *


get_best_markets(pln_btc_mutual)