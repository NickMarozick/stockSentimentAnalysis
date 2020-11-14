import sys
from yahoofinancials import YahooFinancials
from utils import file_utils
from utils import sqlite_utils
from datetime import datetime, timedelta


# connecting to the database
conn = sqlite_utils._createConnection(r"/var/stockSA/stockPricing.db")
if conn is None:
    print("Failed to open database connection")
    sys.exit(1)
sqlite_utils._createStockPricingTable(conn)

print(sqlite_utils._findAllStockPricingBetweenDates(conn, "2020-03-11", "2020-11-14", "AAPL"))


while True :
    ticker = input('Enter a stock symbol or to quit program, type quit: ')
    if ticker == 'quit' :
        quit()

    try: 
        yahoo_financials = YahooFinancials(ticker) 
        # call to the YahooFinance tool function
        historicalStockPrices = yahoo_financials.get_historical_price_data(
                "2020-06-09", "2020-07-08", "daily")
        
        # creating our variable prices, storing all of the data in a list
        if historicalStockPrices[ticker] is None:
            print('Failed to get stock prices')
            continue
        
        prices = historicalStockPrices[ticker]['prices']
        sqlite_utils.insertPrices(conn, ticker, prices)	

    except Exception as e: 
    	print("Invalid StockSymbol, no data ", e)
    	continue


