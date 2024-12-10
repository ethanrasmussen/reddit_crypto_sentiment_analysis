import yfinance as yf
import pandas as pd
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# tickers = [
#     ("Bitcoin", "BTC"),
#     ("Ethereum ", "ETH"),
#     ("Tether", "USDT"),
#     ("Solana", "SOL"),
#     ("Binance", "BNB"), # Technically, "binance coin"
#     ("Ripple", "XRP"),
#     ("Dogecoin", "DOGE"),
#     ("USD Coin", "USDC"), # Including the coin here to ensure not confused with $USD
#     ("Cardano", "ADA"),
#     ("TRON", "TRX")

tickers = ["BTC", "ETH", "USDT", "SOL", "BNB", "XRP", "DOGE", "USDC", "ADA", "TRX"]

# Get full yfinance attribute data for each ticker
def getAllCryptoMetrics(tickers):
    tickersData = {}
    for ticker in tickers:
        tickerObject = yf.Ticker(ticker)

        dataFrame = pd.DataFrame.from_dict(tickerObject.info, orient="index")
        dataFrame.reset_index(inplace=True)
        dataFrame.columns = ["Attribute", "Recent"]

        tickersData[ticker] = data_frame
    return tickersData

# Get current data about current market price, P/E ratio, 52week high and low, and
# averageVolume the last 24 hours on each ticker
def getCurrentMetrics(tickers):
    tickersData = {}
    for ticker in tickers:
        dataObject = {}
        tickerObject = yf.Ticker(ticker)

        dataObject['regularMarketPrice'] = tickerObject.info.get('regularMarketPrice')
        dataObject['forwardPE'] = tickerObject.info.get('forwardPE')
        dataObject['fiftyTwoWeekLow'] = tickerObject.info.get('fiftyTwoWeekLow')
        dataObject['fiftyTwoWeekHigh'] = tickerObject.info.get('fiftyTwoWeekHigh')
        dataObject['averageVolume'] = tickerObject.info.get('averageVolume')
        dataObject['52WeekChange'] = tickerObject.info.get('52WeekChange')
        tickersData[ticker] = dataObject
        getCurrentMetrics = json.dumps(tickersData, indent=4)
    return getCurrentMetrics

# get historicalData for the past year
def getHistoricalData(tickers):
    historicalData = {}
    for ticker in tickers:
        tickerObject = yf.Ticker(ticker)

        historicalData[ticker] = tickerObject.history(period="ytd", interval="1wk")
    return historicalData

# print(getAllCryptoMetrics(tickers))
print(getCurrentMetrics(tickers))
# print(getHistoricalData(tickers))


# get latest endpoint from coinmarketcap API (historical was remove from free edition)
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'symbol': "BTC,ETH,USDT,SOL,BNB,XRP,DOGE,USDC,ADA,TRX",
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': <API-KEY>,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  formatData = json.dumps(data, indent=4)
  print(formatData)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
