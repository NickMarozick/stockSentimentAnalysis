import sys
from datetime import datetime, timedelta
import recordtype
import re


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


def askUserForDates():
    validStart=0
    while validStart == 0:
        startDate= input("""Input a start date for stock price and article
        data in the format: YYYY-MM-DD\n""")

        validStart= validateDate(startDate)

    endDate= askUserForEndDate(startDate)

    print("Start Date: ", startDate)
    print("End Date: ", endDate)


def validateDate(dateString):
    try:
        date= datetime.strptime(dateString, '%Y-%m-%d')
        #print(date)
        #print("validDate")
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
