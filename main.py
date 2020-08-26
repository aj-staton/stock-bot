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
MINUTE = 60 # 60s = 1 min

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
        
        # Ensure I have not exceeded the allowed amount of call's for the API.
        # The `LIMIT - 4` below is to ensure that the 3 API calls within the
        # loop can be executed.
        if (call_count >= LIMIT - 4):
            call_count = 0
            time.sleep(MINUTE)

        symbol = stock['symbol']
        
        # Grab Pricing data.
        try:
            r = req.get(FIN+'/quote?symbol='+symbol+'&token='+KEY)
        except:
            continue

        call_count += 1
        if (r.status_code == HTTP_OK):
            try:
                price = r.json()['c'] # 'c' is current price.
                #print("No price found.")
            except:
                continue
        else:
            print("Bad HTTP Request. Status Code: " + str(r.status_code))
            if (r.status_code == HTTP_TOOMANY):
                time.sleep(LIMIT)
            continue
        
        # Grab Analyst Target Data (the median, specifically)
        try:
            r = req.get(FIN+'/stock/price-target?symbol='+symbol+'&token='+KEY)
        except:
            continue

        call_count += 1

        if (r.status_code == HTTP_OK):
            try:
                target = r.json()['targetMedian']
            except:
                continue
        else:
            print("Bad HTTP Request. Status Code: " + str(r.status_code))
            if (r.status_code == HTTP_TOOMANY):
                time.sleep(LIMIT)
            continue
        
        if (target == 0 or price == 0):
            continue

        difference = round(float(target)-price, 2)
        growth_ratio = round(float(difference/price), 2)

        print(str(call_count)+","+symbol+","+str(price)+ ","+str(target)+","+\
                            str(difference)+","+str(growth_ratio))
        
        # If the target is greater than price, a stock could be undervalued.
        if (difference > 0):
            under_file.write(symbol+","+str(price)+ ","+str(target)+","+\
                            str(difference)+","+str(growth_ratio)+"\n")
        else:
            over_file.write(symbol+","+str(price)+ ","+str(target)+","+\
                            str(difference)+","+str(growth_ratio)+"\n")

    under_file.close()
    over_file.close()
    
    
