import sys
from news_finders import content_scraper
from news_finders import newsApi
from utils import file_utils
from utils import sqlite_utils



STOCKS = ["AAPL", "ABBV", "TXN"]


date= '2020-01-20'

articles = []
articles = newsApi.getArticlesForMultipleStocks(STOCKS, date)



conn= sqlite_utils._createConnection(r"/tmp/stockSentiment.db")

if conn is None: 
    print("Failed to open database connection")
    sys.exit(1)

sqlite_utils._createStockArticleTable(conn)

sqlite_utils.insertStockArticles(conn, articles)
