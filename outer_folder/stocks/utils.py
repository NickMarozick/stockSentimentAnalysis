import sys
from datetime import datetime, timedelta
import recordtype
import re
import requests
from .models import PriceData, StockLoser, StockSymbol, StockGainer

FIELDS = ['stockSymbol', 'name', 'url', 'content', 'description', 'scraper', 'date']

Article = recordtype.recordtype('Article', FIELDS)

def createArticle(*FIELDS):
    return Article(*FIELDS)


def getMaxDateForStockArticles()->str:
    """ This function uses datetime to calculate the maximum date from today
    that can be utilized with the news finders and returns a reformatedDate

    Returns:
        reformatedDate in the form: "MM-DD-YYYY"
    """
    date = datetime.today() - timedelta(days=28)
    reformatedDate= str(date.month) + "-" + str(date.day) + "-" + str(date.year)
    return reformatedDate

def getFormattedDateForNDaysAgo(number_of_days):
    """ This function takes in user input for how many previous days back to
    look for stock articles with a max allowable input of 28.

    Args:
        number_of_days: int number provided by user.
    Returns:
        reformatedDate in the form: "MM-DD-YYYY"
    """
    if number_of_days > 28:
        print("number_of_days specified is greater than 28 which is not allowed - defaulting to max 28")
        number_of_days = 28
    date = datetime.today() - timedelta(days=number_of_days)
    reformatedDate= str(date.month) + "-" + str(date.day) + "-" + str(date.year)
    return reformatedDate

def getTodaysDate():
    """
    This function gets todays date

    Returns:
        reformatedDate in the form: "YYYY-MM-DD"
    """
    date= datetime.today()
    reformatedDate= str(date.year) + "-" + str(date.month) + "-" + str(date.day)
    return reformatedDate


def transform_date_for_yahoo_financials(date):
    """
    Returns:
        reformatedDate in the form: "YYYY-MM-DD"
    """
    reformatedDate= str(date.year) + "-" + str(date.month) + "-" + str(date.day)
    return reformatedDate




def getTodaysDateWithHour():
    """
    This function gets todays date with hour

    Returns:
        reformatedDate in the form: "YYYY-MM-DD HH"
    """
    date= datetime.today()
    reformatedDate= ( str(date.year) + "-" + str(date.month) + "-" +
                      str(date.day) + " " + str(date.hour) )
    return reformatedDate

def increment_date(dateInput):
        '''
        This function takes a date string in the format (YYYY-MM-DD), converts
        into a datetime object, increments by one day, converts the datetime
        back into a formatted string, and returns the incremented date string. Used for
        yahooFinancials

        Input : date string in the format YYYY-MM-DD

        Returns: date string in the format YYYY-MM-DD, incremented by one day
        '''
        dateInput = dateInput.split("-")
        datetime_date = datetime(int(dateInput[0]), int(dateInput[1]), int(dateInput[2]))
        datetime_date += timedelta(days=1)

        incremented_date = str(datetime_date.year) + "-" + str(datetime_date.month) + "-" + str(datetime_date.day)

        return incremented_date

def compareArticleDates(latest_database_date, max_date):
    '''
    This function compares two different formatted dates, one from
    our article database in the format "YYYY-MM-DD" and the max amount of days
    that we can dig up article data from (1 month prior) in the format
    "MM-DD-YYYY". Whichever date is later is returned in the format "MM-DD-YYYY",
    which our newsAPI prefers for queries.
    '''
    latest_database_date = latest_database_date.split("-")
    datetime_database_date = datetime(int(latest_database_date[0]), int(latest_database_date[1]), int(latest_database_date[2]))

    max_date = max_date.split("-")
    datetime_max_date = datetime(int(max_date[2]), int(max_date[0]), int(max_date[1]))

    if datetime_database_date > datetime_max_date:
        # if the database has a closer date to present than max date, return database date
        search_from_date = latest_database_date[1] + "-" + latest_database_date[2] + "-" + latest_database_date[0]
        #print(search_from_date)
        return search_from_date
    else:
        # if max date is closer to present than the database date or equal, return max date
        search_from_date = max_date[0] + "-" + max_date[1] + "-" + max_date[2]
        #print(search_from_date)
        return search_from_date


def askUserForDates():
    """
    This function takes in user input for start date and end date in the format: YYYY-MM-DD

    Returns:
        returns 4 values of formatted start dates for the different utils in the following order:
        startDate: YYYY-MM-DD   (works for stockData pricing)
        endDate: YYYY-MM-DD     (works for stockData pricing)
        reformattedStartDate: MM-DD-YYYY     (works for newsApi stockArticles)
        reformattedEndDate: MM-DD-YYYY       (works for newsApi stockArticles)

    """
    validStart=0
    while validStart == 0:
        startDate= input("""Input a start date for stock price and article
        data in the format: YYYY-MM-DD\n""")

        validStart= validateDate(startDate)

    endDate= askUserForEndDate(startDate)

    reformattedStartDate, reformattedEndDate = adaptDateForSources(startDate, endDate)

    return startDate, endDate, reformattedStartDate, reformattedEndDate



def adaptDateForSources(startDate, endDate):
    """
    This function takes in input for start date and end date in the format: YYYY-MM-DD

    Returns:
        reformatedDate in the form: "MM-DD-YYYY"
    """
    startDatetime= datetime.strptime(startDate, '%Y-%m-%d')
    endDatetime= datetime.strptime(endDate, '%Y-%m-%d')

    reformattedStartDate= str(startDatetime.month) + "-" + str(startDatetime.day) + "-" + str(startDatetime.year)
    reformattedEndDate= str(endDatetime.month) + "-" + str(endDatetime.day) + "-" + str(endDatetime.year)

    return reformattedStartDate, reformattedEndDate

def validateDate(dateString):
    try:
        date= datetime.strptime(dateString, '%Y-%m-%d')

        todaysDate= getTodaysDate()
        if dateString > todaysDate:
            print("Invalid date: future date entered")
            return 0;
        else:
            return 1;
    except:
        print("Invalid date: Input date must be YYYY-MM-DD. Month input max 12, day input max 31 (on select months)\n")
        return 0;


def askUserForEndDate(startDate):
    valid=0
    while valid==0:
        endDate= input("""\nInput an end date for the stock price and article
        data in the format: YYYY-MM-DD\n""")
        if validateDate(endDate) == 0:
            continue
        elif startDate > endDate:
            matched=None
            print("Invalid end date: it is earler than the start date\n")
            continue
        valid=1

    return endDate


def getStockTickersFromUser():
    """ This function asks the user to input individual or multiple stock
    tickers comma seperated that the user would like analyzed

    Returns:
        an array of stock tickers
    """
    stocks=""

    stockArray=[]

    done=0

    while done == 0:

        stocks= input("Input individual stock ticker to analyze or multiple comma seperated stock tickers. If done, write 'done'\n")

        stocks= stocks.split(',')

        for stock in stocks:
            stock= stock.strip(" ")

            if stock == "done":
                done=1
                break

            elif stock in stockArray :
                continue

            else:
                stockArray.append(stock)

    return stockArray

def adaptTradeVolume(tradeVolume):
    """ This function takes the trade volume string from
    our scraper and turns it into an int, formatting correctly
    for our database, removing commas and multiplying out
    data with an 'M' designated for million
    """

    formatted_trade_volume = tradeVolume

    # removing any commas
    formatted_trade_volume = formatted_trade_volume.replace(',','')

    # multiplying out if the string designated has an M
    if formatted_trade_volume[-1] == 'M':
        formatted_trade_volume = float(formatted_trade_volume[:-1])
        # multiply decimal by 1 million for conversion
        formatted_trade_volume = formatted_trade_volume * 1000000

    # converting to an int
    formatted_trade_volume = int(formatted_trade_volume)
    return formatted_trade_volume

def is_valid_stock_symbol(input: str):
    """
    This function takes in a string representing a user input stock
    symbol. The input is appended to the market watch url. If the url returns a
    200 code, then market watch has the stockSymbol registered and the input is
    valid
    Input: String
    Output: 0 if the string is not a valid stock symbol, 1 if it is valid
    """
    url = 'https://www.marketwatch.com/investing/stock/' + input
    request = requests.get(url)

    if request.url == url:
        print('Valid Stock Symbol, %s' % input)
        return 1
    else:
        print('%s is not a stockSymbol' % input)
        return 0
