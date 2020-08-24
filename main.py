# This script will grab the current price of stocks,
# compare to analyst's price targets, and give those
# with the highest price/target ratio.
#
# Written by: Austin Staton
# Date: Aug 21st, 2020

import requests as req
from keys import *
import lib
import json
import time

FIN = 'https://finnhub.io/api/v1' # API's URL
LIMIT = 60 # My free key gets sixty calls per minute. 

# @breif: updateStockList() will update the group of Stocks
#         collected in from the `symbol` API call.
def updateStockList():
    # Grab a list of supported stocks by the API
    stocks = req.get(FIN + '/stock/symbol?exchange=US&token=' + KEY)
    with open("data/stock_list.json", "w") as f:
        json.dump(stocks.json(), f)

if __name__ == '__main__':
    updateStockList()
    call_count = 1 # This is a counter for the calls I make to the API.
    
    # Grab all tickers from the NYSE.
    data = open("data/stock_list.json",)
    stocks = json.load(data)
    data.close()
    
    # Split output files into two for my own organization.
    under_file = open('data/undervalued.csv', 'w+')
    under_file.write("symbol,current_price,target_price,difference,growth_ratio\n")
    under_file.close()
    over_file = open('data/overvalued.csv', 'w+')
    over_file.write("symbol,current_price,target_price,difference,growth_ratio\n")
    over_file.close()

    under_file = open ('data/undervalued.csv', 'a')
    over_file = open('data/overvalued.csv', 'a')

    # Go through all stock tickers and look for analyst projects (if existing).
    for stock in stocks:
       
        symbol = stock['symbol']
        
        # Grab Pricing data.
        r = req.get(FIN+'/quote?symbol='+symbol+'&token='+KEY)
        call_count += 1
        if (r.status_code == 200):
            try:
                price = r.json()['c'] # 'c' is current price.
            except:
                continue
        else:
            print("Bad HTTP Request. Check URL and API call limits.")
            break
        
        # Grab Analyst Target Data (the median, specifically)
        r = req.get(FIN+'/stock/price-target?symbol='+symbol+'&token='+KEY)
        call_count += 1

        if (r.status_code == 200):
            try:
                target = r.json()['targetMedian']
            except:
                continue
        else:
            print("Bad HTTP Request. Check URL and API call limits.")
            break
        
        if (target == 0 or price == 0):
            continue

        difference = round(float(target)-price, 2)
        growth_ratio = round(float(target/price), 2)

        print(symbol+","+str(price)+ ","+str(target)+","+\
                            str(difference)+","+str(growth_ratio)+"\n")
        
        # If the target is greater than price, a stock could be undervalued.
        if (difference > 0):
            undervalued.write(symbol+","+str(price)+ ","+str(target)+","+\
                            str(difference)+","+str(growth_ratio)+"\n")
        else:
            overvalued.write(symbol+","+str(price)+ ","+str(target)+","+\
                            str(difference)+","+str(growth_ratio)+"\n")
        # API Rate-Throttling to ensure no 429 statuses.
        if (call_count >= LIMIT - 3):
            time.sleep(60) # This is a rate-limited API.

    undervalued.close()
    overvalued.close()
    
