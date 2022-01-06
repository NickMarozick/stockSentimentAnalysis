import sys
from yahoofinancials import YahooFinancials
from utils import helper_functions
from utils import sqlite_utils

def setTicker(ticker):
    yahoo_financials= YahooFinancials(ticker)
    return yahoo_financials

def getStockDataAllTime(ticker):
    today = helper_functions.getTodaysDate()
    yahoo_financials = setTicker(ticker)
    historicalStockPrices = yahoo_financials.get_historical_price_data(
        "1816-01-01", today, "daily")
    prices = historicalStockPrices[ticker]["prices"]
    return prices

# New Function
def get_stock_data_from_date(ticker, date):
    today = helper_functions.getTodaysDate()
    yahoo_financials = setTicker(ticker)
    historicalStockPrices = yahoo_financials.get_historical_price_data(date,
        today, "daily")
    prices = historicalStockPrices[ticker]["prices"]
    return prices

# needs edits to match (checking pricing first )
def getAndStoreStockPricingData(ticker, conn):
    prices = getStockDataAllTime(ticker)
    sqlite_utils.insertPrices(conn, ticker, prices)

def getAndStoreMultipleStocksPricingData(stocks, conn):
    for stock in stocks:
        # checks if price data exists for a stock entry
        last_stock_price_entry_date = sqlite_utils.check_if_stored_price_data_for_input_symbol(conn, stock)

        if last_stock_price_entry_date == "None":
            prices = getStockDataAllTime(stock)

        elif last_stock_price_entry_date is None:
            prices = getStockDataAllTime(stock)
            
        else:
            # increment date so that we don't duplicate entries
            incremented_date = helper_functions.incrementDate(last_stock_price_entry_date)
            prices = get_stock_data_from_date(stock, incremented_date)

        sqlite_utils.insertPrices(conn, stock, prices)

def _getPriceDataForTicker(ticker, conn):
    try:
        prices = getStockDataAllTime(ticker)
        getAndStoreStockPricingData(ticker, conn)
    except Exception as e:
        print("Invalid StockSymbol!")


def userSearchAndStoreStockPricingLoop(conn):
    """Search and store prices for stock based on user input.

    Args:
        conn: <class name of conn... same as type(conn)>
    """
    while True:
        tickers = input("Enter stock symbol(s) (e.g., APPL,AMC) or 'quit' to "
                        "end: ")
        if tickers == "quit" :
            break
        else:
            if "," in tickers:
                ticker = ticker.strip()
                for ticker in tickers.split(","):
                    _getPriceDataForTicker(ticker, conn)
            else:
                _getPriceDataForTicker(ticker, conn)
