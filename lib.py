# A group of supporting functions the stock bot might use

# Written by: Austin Staton
# Date: Aug 21st, 2020

import json # Interpreting JSON
import requests as req # Grabbing RESTful API data.

HTTP_BADGATE = 502
HTTP_TOOMANY = 429
HTTP_OK = 200

# @brief: takes in a list, prints all items to console line-by-line
def printList(items):
    for item in items:
        print(item)

def restGetData(resource_id):
    try:
        r = req.get(resource_id)
        return r.json()
    except:
        print("Could not get data.") 
        return []
    
