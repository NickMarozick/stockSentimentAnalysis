import re
import sqlite3
from sqlite3 import Error
import pandas

#database connection  
 
def _createConnection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    #finally:
    #    if conn:
    #        conn.close()
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

# Find Stock Articles per Stock Symbol and After Given Date
# YYYY-MM-DD date format 


def _findAllStockArticlesAfterProvidedDate(conn, inputDate, inputSymbol):
    sql = 'SELECT * FROM stockArticles WHERE date > ? AND stockSymbol=? ORDER BY date DESC'

    try:
        cur = conn.cursor()
        cur.execute(sql, (inputDate, inputSymbol))
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)


# Find Stock Articles per Stock Symbol and Before Given Date


def _findAllStockArticlesBeforeProvidedDate(conn, inputDate, inputSymbol):
    sql = 'SELECT * FROM stockArticles WHERE date < ? AND stockSymbol=? ORDER BY date DESC'

    try:
        cur = conn.cursor()
        cur.execute(sql, (inputDate, inputSymbol))
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)


# Find Stock Articles per Stock Symbol Between a Date Range 
# YYYY-MM-DD format

def _findAllStockArticlesBetweenDates(conn, startDate, endDate, inputSymbol):
    sql = 'SELECT * FROM stockArticles WHERE date >= ? AND date <= ? AND stockSymbol=? ORDER BY date DESC'

    try:
        cur = conn.cursor()
        cur.execute(sql, (startDate, endDate, inputSymbol))
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)



# ------------------------------------------
#dates should be in YYYY-MM-DD format for searching

def _findAllStockPricingBetweenDates(conn, startDate, endDate, inputSymbol):
    sql = 'SELECT * FROM stockPricing WHERE date >= ? AND date <= ? AND stockSymbol=? ORDER BY date DESC'

    try:
        cur = conn.cursor()
        cur.execute(sql, (startDate, endDate, inputSymbol))
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)

# ------------------------------------------


def _findAllStockPricingForStockSymbol(conn, inputSymbol):
    sql= 'SELECT date, close FROM stockPricing WHERE stockSymbol= ? ORDER BY date DESC'

    try:
        cur = conn.cursor()
        cur.execute(sql, (inputSymbol,))
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)



