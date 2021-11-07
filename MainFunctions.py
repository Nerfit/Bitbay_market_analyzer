from BitbayApi import Bitbay_Api
import pandas as pd

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
usdt_markets = [x for x in markets_keys if '-USDT' in x]
# Find mutual markets with PLN currency
pln_btc_mutual = [x.split('-')[0] for x in pln_markets if x.split('-')[0] + '-BTC' in btc_markets]
pln_eth_mutual = [x.split('-')[0] for x in pln_markets if x.split('-')[0] + '-ETH' in eth_markets]
pln_usdt_mutual = [x.split('-')[0] for x in pln_markets if x.split('-')[0] + '-USDT' in usdt_markets]

# Crypto-crypto fee: 0.1%
crypto_crypto_fee = 0.001
# Crypto-FIAT fee (worst scenario): 0.38%
crypto_fiat_fee = 0.0038
# Money to spend
moneyPLN = 15000

def get_best_markets(all_mutual_markets=None, rynek=None):
    """
    Function used to check wheater it is profitable to buy cryptocurrency, sell it instantly on other market and then sell it again to get money in PLN
    :param all_mutual_markets: Define which marker pairs to check
    :param rynek: CryptoCurrency that will be exchanged to PLN
    :return: List of the best profitable transactions (or the least non-profitable ones :D )
    """
    affordable_markets = []
    for market in all_mutual_markets:
        lowest_ask_market = round(float(res['items'][market + '-' + 'PLN']['lowestAsk']), 8)
        highest_bid_rynek = round(float(res['items'][market + '-' + rynek]['highestBid']), 8)
        highest_bid_PLN = round(float(res['items'][rynek + '-PLN']['highestBid']), 8)

        bought_market = round(moneyPLN/lowest_ask_market * (1-crypto_fiat_fee),8)
        bought_rynek = round(bought_market * highest_bid_rynek * (1-crypto_crypto_fee),8)
        obtained_PLN = round(bought_rynek * highest_bid_PLN * (1-crypto_fiat_fee),8)
        saldo = round(obtained_PLN - moneyPLN,2)

        affordable_markets.append([market, bought_market, bought_rynek, obtained_PLN, saldo])
    headers = ['Waluta', 'Kupiona waluta', f'Kupiony {rynek}', 'PLN po wymianie', 'Saldo [PLN]']
    summary = pd.DataFrame(affordable_markets, columns=headers).set_index('Waluta')
    summary = summary.sort_values(by=['Saldo [PLN]'], ascending=False)
    return summary


num = 5
summary = get_best_markets(all_mutual_markets=pln_btc_mutual, rynek='BTC')
print('BTC market')
print(summary.head(num))
summary = get_best_markets(all_mutual_markets=pln_eth_mutual, rynek='ETH')
print('ETH market')
print(summary.head(num))
summary = get_best_markets(all_mutual_markets=pln_usdt_mutual, rynek='USDT')
print('USDT market')
print(summary.head(num))