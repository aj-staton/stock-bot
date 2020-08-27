# A group of supporting functions the stock bot might use

# Written by: Austin Staton
# Date: Aug 21st, 2020

import json # Interpreting JSON
import requests as req # Grabbing RESTful API data.

HTTP_BADGATE = 502
HTTP_TOOMANY = 429
HTTP_OK = 200

MINUTE = 60 # My API key gets 60 free requests per minute.
LIMIT = 60 # 60 Seconds, 1 minute
# @brief: takes in a list, prints all items to console line-by-line
def printList(items):
    for item in items:
        print(item)

# @brief: restGetData() will query a REST API and
#         get the JSON data from the request. Any bad responses
#         will return an empty list.
# 
# @params: uri -- a STRING of the API's universal resource id.
#          endpoint -- a STRING representing the specific enpoint to query.
#          keys -- a LIST of the JSON keys that will be used in request.
#                  They should be checked for inclusion in the data.

# @return: a LIST storing the JSON response from the request.
def restGetData(uri, endpoint, keys):
    try:
        r = req.get(uri + endpoint)
        if (r.status_code != HTTP_OK):
            print("Bad HTTP request. Code: ", str(r.status_code))
            if (r.staus_code == HTTP_TOOMANY):
                time.sleep(MINUTE)
                return []
    except:
        print("Could not get data.") 
        return []

    # Validate that the values that will be used to access data actually exist.
    for key in keys:
        if (not key in r.json()):
            print("error: value does not exist in object.")
            return []

    return r.json()
