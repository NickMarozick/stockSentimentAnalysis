import sys
from datetime import datetime, timedelta
import recordtype


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
