# This script will grab the current price of stocks,
# compare to analyst's price targets, and give those
# with the highest price/target ratio.
#
# Written by: Austin Staton
# Date: Aug 21st, 2020

import requests as req
from keys import *
from lib import *
import json
import time

URI = 'https://finnhub.io/api/v1' # Finnhub's APU URI
LIMIT = 60 # My free key gets sixty calls per minute. 
MINUTE = 60 # 60s = 1 min

# @breif: updateStockList() will update the group of Stocks
#         collected in from the `symbol` API call.
def updateStockList():
    # Grab a list of supported stocks by the API
    stocks = restGetData(URI,'/stock/symbol?exchange=US&token=' + KEY, [])
    with open("data/stock_list.json", "w") as f:
        json.dump(stocks, f)

if __name__ == '__main__':
    updateStockList()
    
    call_count = 1 # This is a counter for the calls I make to the API.
    
    # Grab all tickers from the NYSE.
    data = open("data/stock_list.json",)
    stocks = json.load(data)
    data.close()
    
    # Open output files in the `data` folder.
    out_file = open('data/stock-data.csv', 'w+')
    out_file.write("Symbol,Name,Current Price,Target Low,Target Median,Target \
                      High,Difference,ROI Potential\n")
    out_file.close()

    out_file = open ('data/stock-data.csv', 'a')

    # Go through all stock tickers and look for analyst projects (if existing).
    for stock in stocks:
        
        # Ensure I have not exceeded the allowed amount of call's for the API.
        # The `LIMIT - 4` below is to ensure that the 3 API calls within the
        # loop can be executed.
        if (call_count >= LIMIT - 4):
            call_count = 0
            time.sleep(MINUTE)

        symbol = stock['symbol']
        name = stock['description']

        # Grab Pricing data.
        price_data = restGetData(URI, '/quote?symbol='+symbol+'&token='+\
                        KEY, ['c'])
        call_count += 1
        if (price_data == []):
            continue
        curr_price = price_data['c']
        
        # Grab Analyst Target Data (the median, specifically)
        target_data = restGetData(URI, '/stock/price-target?symbol='+symbol\
                        +'&token='+KEY, ['targetMedian', 'targetLow',
                        'targetHigh'])
        call_count += 1
        if (target_data == []):
            continue

        target = target_data['targetMedian']
        target_low = target_data['targetLow']
        target_high = target_data['targetHigh']

        if (target == 0 or curr_price == 0):
            continue

        difference = round(float(target)-curr_price, 2)
        roi = round(float(difference/curr_price), 2)

        print(str(call_count)+","+symbol+","+str(curr_price)+ ","+str(target)+","+\
                            str(difference)+","+str(roi))
        
        output = symbol+","+name+","+str(curr_price)+","+\
                 str(target_low)+","+str(target)+","+str(target_high)+","+\
                 str(difference)+","+str(roi)
        out_file.write(output)
      
    out_file.close()
