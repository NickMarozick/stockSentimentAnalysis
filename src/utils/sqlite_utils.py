
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
    finally:
        if conn:
            conn.close()
 

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

def _insertStockArticle(conn, article):
    
    sql = 'INSERT INTO stockArticles(stockSymbol, name, url, content, description, scraper, date) VALUES({}, {}, {}, {}, {}, {}, {})'
          
    try:
        cur = conn.cursor()
        cur.execute(sql.format(article.stockSymbol, article.name, article.url, article.content, article.description, article.scraper, article.date))
        conn.commit()
        return cur.lastrowid
    except Error as e:
         print(e)


def insertStockArticles(articles):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        for article in articles: 
            _insertStockArticle(conn, article)
     except Error as e:
         print(e)     


def _findStockArticlesForSymbol(conn, stockSymbol):    
    sql = 'SELECT * FROM stockArticles WHERE stockSymbol=?' 
   
    try:
        cur = conn.cursor()
        cur.execute(sql, (stockSymbol,))         
        rows= cur.fetchall()
        return rows
    except Error as e:
         print(e)


