import requests
from utils import helper_functions
from utils import sqlite_utils


def getArticlesForMultipleStocks(stocks, date):
    listArticles=[]
    for stock in stocks:
        articles = getArticlesForStock(stock, date)
        listArticles.extend(articles)
    return listArticles

def getAndStoreArticlesForMultipleStocks(stocks, date, conn):
    listArticles= []

    for stock in stocks:
        last_article_entry_date = sqlite_utils.check_if_stored_article_data_for_input_symbol(conn, stock)
        print(last_article_entry_date)
        if last_article_entry_date == "None":
            articles = getArticlesForStock(stock, date)
        elif last_article_entry_date is None:
            articles = getArticlesForStock(stock, date)
        else:
            revisedDate = helper_functions.incrementDate(last_article_entry_date)
            search_from_date = helper_functions.compareArticleDates(revisedDate, date)
            articles = getArticlesForStock(stock, search_from_date)
        #articles = getArticlesForStock(stock, date)
        listArticles.extend(articles)
    sqlite_utils.insertStockArticles(conn, listArticles)

def getArticlesForStock(stockSymbol, date):
    url_pattern = ('https://newsapi.org/v2/everything?'
        'q={0}+stock&'
        'from={1}&'
        'sortBy=popularity&'
        'apiKey=ec07e0116ce8450c8b677e877b2e8761')
    url= url_pattern.format(stockSymbol, date)
    response = requests.get(url).json()


    if response["status"]=="error":
        print(response["message"])
        exit()


    listArticles= []
    for article in response["articles"]:
        newTuple= helper_functions.createArticle(
            stockSymbol, article.get('title'), article.get('url'),
            article.get('content'), article.get('description'),
            "NewsAPI", article.get('publishedAt')[:10])
        listArticles.append(newTuple)
    return listArticles
