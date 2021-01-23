import sys
from news_finders import content_scraper
from news_finders import newsApi
from utils import sqlite_utils
from utils import helper_functions

#STOCKS = ["AAPL", "ABBV", "TXN"]

STOCKS = ["NFLX", "NKE", "NVDA"]

#date= datetime.today() - timedelta(days=28)

#reformatedDate= str(date.month) + "-" + str(date.day) + "-" + str(date.year)

get_articles_from_this_date = helper_functions.getMaxDateForStockArticles()
print("back date: ", get_articles_from_this_date)

articles = []
articles = newsApi.getArticlesForMultipleStocks(STOCKS, get_articles_from_this_date)
print(articles)


conn= sqlite_utils.createConnection(r"/var/stockSA/stockSentiment.db")

if conn is None:
    print("Failed to open database connection")
    sys.exit(1)

#sqlite_utils._createStockArticleTable(conn)

sqlite_utils.insertStockArticles(conn, articles)

print(sqlite_utils._findStockArticlesForSymbol(conn, "NVDA")[0])

#print(sqlite_utils._findAllStockArticlesAfterProvidedDate(conn, "2020-03-09", "AAPL"))

#print(sqlite_utils._findAllStockArticlesBetweenDates(conn, "2020-03-09", "2020-11-14", "AAPL"))
