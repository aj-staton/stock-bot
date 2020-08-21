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

LIMIT_CALLS = True

# @breif: updateStockList() will update the group of Stocks
#         collected in from the `symbol` API call. This is done
#         in this function once, optionally, because I want to
#         limit calls to the API.
def updateStockList():
    # Grab a list of supported stocks by the API
    stocks = req.get(FINN + '/symbol?exchange=US&token=' + KEY)
    with open("stock_list.json", "w") as f:
        json.dump(stocks.json(), f)

if __name__ == '__main__':
    if (not LIMIT_CALLS):
        updateStockList()

    data = open("stock_list.json",)
    stocks = json.load(data)
    data.close()
    
    for stock in stocks['symbol']:
        print(stock)
