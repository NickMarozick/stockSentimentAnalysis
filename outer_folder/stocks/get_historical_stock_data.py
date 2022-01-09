import sys
from yahoofinancials import YahooFinancials
from datetime import datetime
from django.db.models import Max
import stocks.utils as utils
from .models import PriceData, StockLoser, StockSymbol, StockGainer


def get_or_save_stock_symbol_id(ticker):
    valid = utils.is_valid_stock_symbol(ticker)

    if valid:
        try:
            id = StockSymbol.objects.get(name=ticker).id
            return id
        except:
            try: 
                app = StockSymbol.objects.create(name=ticker)
                return app.id
            except Exception as e:
                print('save failed: ', e)
            return
    else:
        print("Invalid Stock Symbol: %s" % ticker)
        return

def set_ticker(ticker):
    yahoo_financials= YahooFinancials(ticker)
    return yahoo_financials

def get_stock_data_all_time(ticker):
    today = utils.getTodaysDate()
    yahoo_financials = set_ticker(ticker)
    historicalStockPrices = yahoo_financials.get_historical_price_data(
        "1816-01-01", today, "daily")
    prices = historicalStockPrices[ticker]["prices"]
    return prices

def get_stock_data_from_date(ticker, date):
    today = utils.getTodaysDate()
    yahoo_financials = set_ticker(ticker)
    historicalStockPrices = yahoo_financials.get_historical_price_data(date,
        today, "daily")
    prices = historicalStockPrices[ticker]["prices"]
    return prices

# ideally would like checker on what price data already exists (save time)
def get_and_store_stock_pricing_data(ticker):
    prices = get_stock_data_all_time(ticker)
    try:
        id = get_or_save_stock_symbol_id(ticker)
        for price in prices:
            try:
                PriceData.objects.create(stock_id=id, date=price['formatted_date'], open=price['open'],
                    close=price['close'], volume=price['volume'])
            except Exception as e:
                print ("Could not create PriceData object. Error: %s\n" % e)
        print("Finished retrieving and storing price data for %s\n" % ticker)
        return
    except Exception as e:
        print("Error in attempting to save price data for %s stock: %s" % (ticker, e))
        return
    return
        

def get_adnd_store_multiple_stocks_pricing_data(stocks):
    for stock in stocks:
        # checks if price data exists for a stock entry
        last_stock_price_entry_date = sqlite_utils.check_if_stored_price_data_for_input_symbol(conn, stock)

        if last_stock_price_entry_date == "None":
            prices = get_stock_data_all_time(stock)

        elif last_stock_price_entry_date is None:
            prices = get_stock_data_all_time(stock)
            
        else:
            # increment date so that we don't duplicate entries
            incremented_date = utils.incrementDate(last_stock_price_entry_date)
            prices = get_stock_data_from_date(stock, incremented_date)

        sqlite_utils.insertPrices(conn, stock, prices)

def get_stock_most_current_price_data_date(ticker):
    """
    Returns:
        Latest date for price data retrieved (if any) or default date
    """
    id = get_or_save_stock_symbol_id(ticker)
    print("id: ", id)

    if id:
        try:
            # date_dict of None creates an issue, need to address logic (change to default date)
            date_dict = PriceData.objects.filter(stock_id=id).aggregate(Max('date'))
            revised_date = transform_date_for_yahoo_financials(date_dict['date__max'])
            return revised_date

        except Exception as e:
            print("Error in getting most current price data date: %s" % e)
            return 

    else: 
        print("Was unable to retrieve stock id\n")
        return

def transform_date_for_yahoo_financials(date):
    """
    Returns:
        reformatedDate in the yahooFinancials expected format: "YYYY-MM-DD"
    """
    reformatedDate= str(date.year) + "-" + str(date.month) + "-" + str(date.day)
    return reformatedDate

def get_todays_date_yahoo_financials():
    """
    Returns:
        reformatedDate in the yahooFinancials expected format: "YYYY-MM-DD"
    """
    date= datetime.today()
    reformatedDate= str(date.year) + "-" + str(date.month) + "-" + str(date.day)
    return reformatedDate


def _get_price_data_for_ticker(ticker, conn):
    try:
        prices = get_stock_data_all_time(ticker)
        get_and_store_stock_pricing_data(ticker, conn)
    except Exception as e:
        print("Invalid StockSymbol!")


def user_search_and_store_stock_pricing_loop(conn):
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
                    _get_price_data_for_ticker(ticker, conn)
            else:
                _get_price_data_for_ticker(ticker, conn)