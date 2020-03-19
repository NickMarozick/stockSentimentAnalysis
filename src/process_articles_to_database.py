import sys
from news_finders import content_scraper
from news_finders import newsApi
from utils import file_utils
from utils import sqlite_utils



STOCKS = ["AAPL", "ABBV", "TXN"]


date= '2020-03-04'

articles = []
articles = newsApi.getArticlesForMultipleStocks(STOCKS, date)



conn= sqlite_utils._createConnection(r"/var/stockSA/stockSentiment.db")

if conn is None: 
    print("Failed to open database connection")
    sys.exit(1)

#sqlite_utils._createStockArticleTable(conn)

#sqlite_utils.insertStockArticles(conn, articles)
print(sqlite_utils._findStockArticlesForSymbol(conn, "AAPL")[0])
