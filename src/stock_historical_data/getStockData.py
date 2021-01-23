import sys
from yahoofinancials import YahooFinancials
from utils import helper_functions
from utils import sqlite_utils

def setTicker(ticker):
    yahoo_financials= YahooFinancials(ticker)
    return yahoo_financials

def getStockDataAllTime(ticker):
    today= helper_functions.getTodaysDate()
    yahoo_financials= setTicker(ticker)
    historicalStockPrices= yahoo_financials.get_historical_price_data("1816-01-01", today, "daily")
    prices= historicalStockPrices[ticker]['prices']
    return prices

def getAndStoreStockPricingData(ticker, conn):
    prices = getStockDataAllTime(ticker)
    sqlite_utils.insertPrices(conn, ticker, prices)

def userSearchAndStoreStockPricingLoop(conn):
    while True:
        ticker = input('Enter a stock symbol or to quit program, type quit: ')
        if ticker == 'quit' :
            quit()

        try:
            prices= getStockDataAllTime(ticker)
            getAndStoreStockPricingData(ticker, conn)

        except Exception as e:
            print("Invalid StockSymbol, no data", e)
