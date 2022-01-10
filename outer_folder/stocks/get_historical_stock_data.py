import sys
from yahoofinancials import YahooFinancials
from datetime import date, datetime
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

def get_and_store_stock_pricing_data(ticker):
    date = get_stock_most_current_price_data_date(ticker)
    incremented_date = utils.increment_date(date)
    print("Incremented last date price data retrieved: %s. If none, 1/2/1800", incremented_date)
    prices = get_stock_data_from_date(ticker, date)
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
        

def get_and_store_multiple_stocks_pricing_data(stocks):
    for stock in stocks:
        # checks if price data exists for a stock entry
        try: 
            id = get_or_save_stock_symbol_id(stock)
            last_stock_price_entry_date = get_stock_most_current_price_data_date(stock)
            print("Last stock price date: %s" % last_stock_price_entry_date)

            if last_stock_price_entry_date == None:
                print("Could not find price data for likely invalid stock name %s" % stock)

            else:
                # increment date so that we don't duplicate entries
                incremented_date = utils.increment_date(last_stock_price_entry_date)
                prices = get_stock_data_from_date(stock, incremented_date)
                for price in prices:
                    try:
                        PriceData.objects.create(stock_id=id, date=price['formatted_date'], open=price['open'],
                            close=price['close'], volume=price['volume'])
                    except Exception as e:
                        print ("Could not create PriceData object for %s. Error: %s\n" % (price['formatted_date'], e))
        except Exception as e:
            print("Stock input %s likely not a valid stock. Error: %s" %(stock, e))
    print("Finished retrieving and storing price data for all stocks\n")
    return


def get_stock_most_current_price_data_date(ticker):
    """
    Returns:
        Latest date for price data retrieved (if any) or default date
    """
    id = get_or_save_stock_symbol_id(ticker)

    if id:
        try:
            date_dict = PriceData.objects.filter(stock_id=id).aggregate(Max('date'))

            # handles the condition of no date existing for price data 
            if date_dict['date__max'] == None:
                return "1800-01-01" 
            else:
                revised_date = transform_date_for_yahoo_financials(date_dict['date__max'])
                return revised_date

        except Exception as e:
            print("Error in getting most current price data date: %s" % e)
            return 

    else: 
        # condition reached if invalid stock name
        print("Was unable to retrieve or save stock id\n")
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

# def user_search_and_store_stock_pricing_loop():
#     """Search and store prices for stock based on user input.
#     """
#     while True:
#         tickers = input("Enter stock symbol(s) (e.g., APPL,AMC) or 'quit' to "
#                         "end: ")
#         if tickers == "quit" :
#             break
#         else:
#             if "," in tickers:
#                 ticker = ticker.strip()
#                 for ticker in tickers.split(","):
#                     get_and_store_stock_pricing_data(ticker)
#             else:
#                 get_and_store_stock_pricing_data(ticker)
#     print("Finished loop\n")
#     return