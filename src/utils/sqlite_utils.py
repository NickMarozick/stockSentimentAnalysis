import re
import sqlite3
from sqlite3 import Error
import pandas


#database connection
def setUpArticleDatabase():
    connection_article_database = createConnection(r"/var/stockSA/stockSentiment.db")
    _createStockArticleTable(connection_article_database)
    return connection_article_database

def setUpPricingDatabase():
    connection_pricing_database = createConnection(r"/var/stockSA/stockPricing.db")
    _createStockPricingTable(connection_pricing_database)
    return connection_pricing_database

def createConnection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def _createStockArticleTable(conn):

    sql = '''CREATE TABLE IF NOT EXISTS stockArticles(stockSymbol text, name text,
             url text, content text, description text, scraper text, date text, sentiment NULL,
             PRIMARY KEY (stockSymbol, name))'''

    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Error as e:
         print(e)


def _createStockPricingTable(conn):

    sql = '''CREATE TABLE IF NOT EXISTS stockPricing(stockSymbol text, date text,
             low int, high int, opening int, close int, volume int,
             PRIMARY KEY (stockSymbol, date))'''

    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Error as e:
         print(e)


def _insertStockArticle(conn, article):

    sql = 'INSERT INTO stockArticles(stockSymbol, name, url, content, description, scraper, date) VALUES(?, ?, ?, ?, ?, ?, ?)'

    try:
        cur = conn.cursor()

        cur.execute(sql, (article.stockSymbol, article.name, article.url, article.content, article.description, article.scraper, article.date))
        conn.commit()
        return cur.lastrowid
    except Error as e:
         print("Failed to create article", e, article)


def _insertPrice(conn, stockName, price):

    sql = 'INSERT INTO stockPricing(stockSymbol, date, low, high, opening, close, volume) VALUES(?, ?, ?, ?, ?, ?, ?)'

    try:
        cur = conn.cursor()
        cur.execute(sql, (stockName, price['formatted_date'], price['low'], price['high'], price['open'], price['close'], price['volume']))
        conn.commit()
        return cur.lastrowid
    except Error as e:
         print("Failed to create price data", e, price)


def insertStockArticles(conn, articles):
    try:
        for article in articles:
            _insertStockArticle(conn, article)
    except Error as e:
        print(e)


def insertPrices(conn, stockName, prices):
    try:
        for price in prices:
            _insertPrice(conn, stockName, price)
    except Error as e:
        print(e)


def _findStockArticlesForSymbol(conn, stockSymbol):
    sql = 'SELECT * FROM stockArticles WHERE stockSymbol=?'

    try:
        cur = conn.cursor()
        cur.execute(sql, (stockSymbol,))
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(e)


def _findAllStockArticlesAfterProvidedDate(conn, inputDate, inputSymbol):
    sql = 'SELECT * FROM stockArticles WHERE date > ? AND stockSymbol=? ORDER BY date DESC'

    try:
        cur = conn.cursor()
        cur.execute(sql, (inputDate, inputSymbol))
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)


def _findAllStockArticlesBeforeProvidedDate(conn, inputDate, inputSymbol):
    sql = 'SELECT * FROM stockArticles WHERE date < ? AND stockSymbol=? ORDER BY date DESC'

    try:
        cur = conn.cursor()
        cur.execute(sql, (inputDate, inputSymbol))
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)


def _findAllStockArticlesBetweenDates(conn, startDate, endDate, inputSymbol):
    sql = 'SELECT * FROM stockArticles WHERE date >= ? AND date <= ? AND stockSymbol=? ORDER BY date DESC'

    try:
        cur = conn.cursor()
        cur.execute(sql, (startDate, endDate, inputSymbol))
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)


def _findAllStockPricingBetweenDates(conn, startDate, endDate, inputSymbol):
    sql = 'SELECT * FROM stockPricing WHERE date >= ? AND date <= ? AND stockSymbol=? ORDER BY date DESC'

    try:
        cur = conn.cursor()
        cur.execute(sql, (startDate, endDate, inputSymbol))
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)


def _findAllStockPricingForStockSymbol(conn, inputSymbol):
    sql= 'SELECT date, close FROM stockPricing WHERE stockSymbol= ? ORDER BY date ASC'

    try:
        cur = conn.cursor()
        cur.execute(sql, (inputSymbol,))
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)

def check_if_stored_article_data_for_input_symbol(connArticle, inputSymbol: str):
    sql = 'SELECT MAX (date) FROM stockArticles WHERE stockSymbol = ?'

    try:
        cur = connArticle.cursor()
        cur.execute(sql, (inputSymbol,))
        result = cur.fetchone()
        result = result[0]
        return result
    except Error as e:
        print(e)

def check_if_stored_price_data_for_input_symbol(connPricing, inputSymbol: str):
    sql = 'SELECT MAX (date) FROM stockPricing WHERE stockSymbol = ?'

    try:
        cur = connPricing.cursor()
        cur.execute(sql, (inputSymbol,))
        result = cur.fetchone()
        result = result[0]
        return result
    except Error as e:
        print(e)


def fetchStockDataOverview(connPricing, connArticle, STOCKS):
    sqlPricingCount='SELECT COUNT(stockSymbol) FROM stockPricing WHERE stockSymbol = ?'
    sqlPricingMinDate= 'SELECT MIN(date) FROM stockPricing WHERE stockSymbol= ?'
    sqlPricingMaxDate= 'SELECT MAX(date) FROM stockPricing WHERE stockSymbol= ?'
    sqlArticleCount='SELECT COUNT(stockSymbol) FROM stockArticles WHERE stockSymbol= ?'
    sqlArticleMinDate= 'SELECT MIN(date) FROM stockArticles WHERE stockSymbol= ?'
    sqlArticleMaxDate= 'SELECT MAX(date) FROM stockArticles WHERE stockSymbol= ?'

    data={}

    for stock in STOCKS:
        try:
            pricingCur = connPricing.cursor()
            articleCur = connArticle.cursor()

            pricingCur.execute(sqlPricingCount, (stock,))
            pricingRowCount= pricingCur.fetchone()[0]
            pricingCur.execute(sqlPricingMinDate, (stock,))
            pricingMinDate= pricingCur.fetchone()[0]
            pricingCur.execute(sqlPricingMaxDate, (stock,))
            pricingMaxDate= pricingCur.fetchone()[0]

            articleCur.execute(sqlArticleCount, (stock, ))
            articleRowCount=articleCur.fetchone()[0]
            articleCur.execute(sqlArticleMinDate, (stock, ))
            articleMinDate=articleCur.fetchone()[0]
            articleCur.execute(sqlArticleMaxDate, (stock, ))
            articleMaxDate=articleCur.fetchone()[0]

            data[stock]=[pricingRowCount, pricingMinDate, pricingMaxDate, articleRowCount, articleMinDate, articleMaxDate]

        except Error as e:
             print(e)

    print ("{:<8} {:<15} {:<18} {:<18} {:<15} {:<18} {:<18}".format('Ticker','Pricing Rows','Pricing Min Date','Pricing Max Date', 'Article Rows', 'Article Min Date', 'Article Max Date'))
    for k,v in data.items():
        pricingRowCount, pricingMinDate, pricingMaxDate, articleRowCount, articleMinDate, articleMaxDate = v
        print ("{:<8} {:<15} {:<18} {:<18} {:<15} {:<18} {:<18}".format(str(k), str(pricingRowCount), str(pricingMinDate), str(pricingMaxDate), str(articleRowCount), str(articleMinDate), str(articleMaxDate)))
