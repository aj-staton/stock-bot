# Stock Bot
Finding companies to invest in is challenging. This tool aims to fix that. I'm planning to use this script to find companies of interest that I can then give a proper Fundamental Analysis for the potential of investment.

I don't plan to try to perform the Fundamental Analysis with anything on a program. In my own (and most likely naive) opinion, that type of assessment can only be properly performed by a set of human eyes and mind. I'm simply looking to narrow my search here.

## Goals
These scripts will parse all NYSE ticker and look for companies with high growth projections. So, it'll grab a ticker's current price, compare it to the median of analyst projections, and return the companies that have the highest (alleged) room for growth. 

## Use
* Go to [Finnhub's](https://finnhub.io/) website and create an account to get an API key.
* With this key, make a file in the folder called `key.py`. The file should look like this:
```python
KEY="<your api key>"
```
This file gets imported into `main.py` for the data collection.
* Run `make bot`; then, the data will be printed to the console.
