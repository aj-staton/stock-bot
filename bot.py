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
LIMIT_CALLS = True
LIMIT_TIME = 30 # My free key gets thirty calls per second. This will throttle. 
PRICE_DIFFS = dict()

# @breif: updateStockList() will update the group of Stocks
#         collected in from the `symbol` API call.
def updateStockList():
    # Grab a list of supported stocks by the API
    stocks = req.get(FIN + '/stock/symbol?exchange=US&token=' + KEY)
    with open("stock_list.json", "w") as f:
        json.dump(stocks.json(), f)

if __name__ == '__main__':
    updateStockList()

    data = open("stock_list.json",)
    stocks = json.load(data)
    data.close()
    
    write_file = open('data_dump.csv', 'w+')
    write_file.write('symbol,current_price,target-price,difference')
    write_file.close()
    write_file = open ('data_dump.csv', 'a')

    # Go through all stock tickers and look for analyst projects (if existing).
    for stock in stocks:
       
        symbol = stock['symbol']
        
        # Grab Pricing data.
        r = req.get(FIN+'/quote?symbol='+symbol+'&token='+KEY)
        if (r.status_code == 200):
            try:
                price = r.json()['c'] # 'c' is current price.
            except:
                continue
        else:
            print("Bad HTTP Request. Check URL and API call limits.")
            exit(0)
        
        # Grab Analyst Target Data (the median, specifically)
        r = req.get(FIN+'/stock/price-target?symbol='+symbol+'&token='+KEY)
        if (r.status_code == 200):
            try:
                target = r.json()['targetMedian']
            except:
                continue

        write_file.write(symbol+","+str(price)+ ","+str(target)+","+\
                            str(target-price))
        
        time.sleep(2) # This is a rate-limited API.

    write_file.close()
