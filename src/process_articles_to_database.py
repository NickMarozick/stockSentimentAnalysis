import sys
from news_finders import content_scraper
from news_finders import newsApi
from utils import file_utils
from utils import sqlite_utils
from datetime import datetime, timedelta


STOCKS = ["AAPL", "ABBV", "TXN"]


date= datetime.today() - timedelta(days=28)

reformatedDate= str(date.month) + "-" + str(date.day) + "-" + str(date.year)


articles = []
articles = newsApi.getArticlesForMultipleStocks(STOCKS, reformatedDate)



conn= sqlite_utils.createConnection(r"/var/stockSA/stockSentiment.db")

if conn is None:
    print("Failed to open database connection")
    sys.exit(1)

#sqlite_utils._createStockArticleTable(conn)

sqlite_utils.insertStockArticles(conn, articles)

print(sqlite_utils._findStockArticlesForSymbol(conn, "AAPL")[0])

#print(sqlite_utils._findAllStockArticlesAfterProvidedDate(conn, "2020-03-09", "AAPL"))

#print(sqlite_utils._findAllStockArticlesBetweenDates(conn, "2020-03-09", "2020-11-14", "AAPL"))
