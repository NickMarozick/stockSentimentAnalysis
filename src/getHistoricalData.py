import sys
from yahoofinancials import YahooFinancials
from utils import file_utils
from utils import sqlite_utils
from datetime import datetime, timedelta


ticker= 'AAPL'

yahoo_financials = YahooFinancials(ticker)

# call to the YahooFinance tool function 

historicalStockPrices=yahoo_financials.get_historical_price_data("2020-06-09", "2020-07-08", "daily")

# creating our variable prices, storing all of the data in a list 

prices=historicalStockPrices['AAPL']['prices']



# connecting to the database 

conn= sqlite_utils._createConnection(r"/var/stockSA/stockPricing.db")

if conn is None:
    print("Failed to open database connection")
    sys.exit(1)

sqlite_utils._createStockPricingTable(conn)


for price in prices:
    date=price['formatted_date']
    low=price['low']
    high=price['high']
    opening=price['open']
    close=price['close']
    volume=price['volume']
    print(date, low, high, opening, close, volume)

sqlite_utils.insertPrices(conn, ticker, prices)
