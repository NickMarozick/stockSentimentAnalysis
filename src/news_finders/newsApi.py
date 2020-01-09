import requests
import xlsxwriter
import csv

from utils import file_utils

# need to import


def getArticlesForMultipleStocks(STOCKS, date):

    listArticles=[]

    for stock in STOCKS:
 
        articles = getArticlesForStock(stock, date)

        listArticles.append(articles)

    return listArticles


def getArticlesForStock(stockSymbol, date):

    url_pattern = ('https://newsapi.org/v2/everything?'
        'q={0}+stock&'
        'from={1}&'
        'sortBy=popularity&'
       'apiKey=ec07e0116ce8450c8b677e877b2e8761')

    url= url_pattern.format(stock, date)
    response = requests.get(url).json()

    listArticles= []

    for article in response["articles"]:
        newTuple= file_utils.createArticle(stockSymbol, article.get('title'), article.get('url'), article.get('content'), article.get('description'), "NewsAPI", article.get('publishedAt')[:10])

        listArticles.append(newTuple)

      
    return listArticles



stock = "AAPL"
date= '2019-12-15'

STOCKS=["AAPL", "NFLX", "AMD"]

print(getArticlesForStock(stock, date))

print('\n')

print(getArticlesForMultipleStocks(STOCKS, date))
