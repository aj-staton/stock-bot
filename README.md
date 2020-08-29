
# Stock Bot
Finding companies to invest in is challenging. This tool aims to fix that. I'm planning to use this script to find companies of interest that I can then give a proper Fundamental Analysis for the potential of investment.

I don't plan to try to perform the Fundamental Analysis with anything in a computer program. In my own (and probably naive) opinion, that type of assessment can only be properly performed by a set of human eyes and mind. I'm simply looking to narrow my search here.

## Goals
- [X] These scripts will parse all NYSE tickers and look for companies with high growth projections. So, it'll grab a ticker's current price, compare it to the median of analyst projections, and return the companies that have the highest (alleged) room for growth. 
- [ ] Add the ability to input a stock ticker, look up the ticker's peers in the
  market, and rank thier P/E and P/B.

## Execution
* Go to [Finnhub's](https://finnhub.io/) website and create an account to get an API key.
* With this key, make a file in the repo folder called `key.py`. The file should look like this:
```python
KEY="<your api key>"
```
This file gets imported into `main.py` for the data collection.
* There are two `make` targets:`roi` and `pe`. The first, `roi`, will produce data on the projected growth for companies based on analyst targets

### Disclaimers
 * No stock is guaranteed to increase in value. If stocks were always that deterministic, there would be no risk. No data this repository produces should be taken as investment advice.
 * The free version of the Finnhub API is [rate-limited at 60 calls per minute](https://finnhub.io/pricing). Over 10k calls will be needed. Don't be
 in too much of a rush for this data.
 * Some stocks only have one analyst rating; so, if that _one_ analyst thinks the stock price is shooting to the moon, the data will too. This is very common 
 to see on penny stocks. Be able to identify these anomalies. 
