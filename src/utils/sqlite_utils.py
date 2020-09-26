import re
import sqlite3
from sqlite3 import Error


#database connection  
 
def _createConnection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    #finally:
    #    if conn:
    #        conn.close()
    return conn 

# create project 

def _createStockArticleTable(conn):
    
    sql = '''CREATE TABLE IF NOT EXISTS stockArticles(stockSymbol text, name text, 
             url text, content text, description text, scraper text, date text, sentiment NULL, 
             PRIMARY KEY (stockSymbol, name))'''
    
    try:         
        cur = conn.cursor()
        cur.execute(sql) 
    except Error as e: 
         print(e)

# update project 

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
    
    #sql = 'INSERT INTO stockArticles(stockSymbol, name, url, content, description, scraper, date) VALUES({}, {}, {}, {}, {}, {}, {})'
    sql = 'INSERT INTO stockArticles(stockSymbol, name, url, content, description, scraper, date) VALUES(?, ?, ?, ?, ?, ?, ?)'
          
    try:
        cur = conn.cursor()
        #cur.execute(sql.format(article.stockSymbol, re.escape(article.name), re.escape(article.url), re.escape(article.content), re.escape(article.description), re.escape(article.scraper), article.date))
        cur.execute(sql, (article.stockSymbol, article.name, article.url, article.content, article.description, article.scraper, article.date))
        conn.commit()
        return cur.lastrowid
    except Error as e:
         print("Failed to create article", e, article)

def _insertPrice(conn, stockName, price):
    
    #sql = 'INSERT INTO stockPricing(stockSymbol, name, url, content, description, scraper, date) VALUES({}, {}, {}, {}, {}, {}, {})'
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

def _findAllStockArticlesAfterProvidedDate(conn, inputDate):
    sql = 'SELECT * FROM stockArticles WHERE date >= Convert(datetime, inputDate)'

    try:
        cur = conn.cursor()
        cur.execute(sql, inputDate)
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)

# Find All Stock Articles between a date range 
# All Stock 


# ------------------------------------------


# Find Stock Articles per Stock Symbol Between a Date Range 
# Individual Stock 

# ------------------------------------------

# Find Stock Articles per Stock Symbol and After Given Date
# Individual Stock 


# ------------------------------------------

