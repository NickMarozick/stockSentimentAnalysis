import requests
import xlsxwriter
import csv

from utils import file_utils

# need to import


def getArticlePerStocks(STOCKS):
    # return same named tuple

    #stock_info[]

    url_pattern = ('https://newsapi.org/v2/everything?'
       'q={0}+stock&'
       'from={1}&'
       'sortBy=popularity&'
       'apiKey=ec07e0116ce8450c8b677e877b2e8761')

    for stock in STOCKS:
        date = '2019-12-10'
        url = url_pattern.format(stock, date)
        response = requests.get(url).json()

        #articles= response["articles"]


    return articles

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
        newTuple= file_utils.createArticle(stockSymbol, article.get('title'), article.get('url'), article.get('content'), article.get('description'), "NewsAPI")

        listArticles.append(newTuple)


        #namedTuple=(response.get('title'), response.get('url'), response.get('description'), response.get('content'), "NewsAPI") # missing the description field

    return listArticles



stock = "AAPL"
date= '2019-12-15'

print(getArticlesForStock(stock, date))
