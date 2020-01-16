
import csv
import requests
import xlsxwriter

from utils import file_utils


def getArticlesForMultipleStocks(stocks, date):
    listArticles=[]
    for stock in stocks:
        articles = getArticlesForStock(stock, date)
        listArticles.extend(articles)
    return listArticles


def getArticlesForStock(stockSymbol, date):
    url_pattern = ('https://newsapi.org/v2/everything?'
        'q={0}+stock&'
        'from={1}&'
        'sortBy=popularity&'
       'apiKey=ec07e0116ce8450c8b677e877b2e8761')
    url= url_pattern.format(stockSymbol, date)
    response = requests.get(url).json()
    #print(response)
    listArticles= []
    for article in response["articles"]:
        newTuple= file_utils.createArticle(
            stockSymbol, article.get('title'), article.get('url'),
            article.get('content'), article.get('description'),
            "NewsAPI", article.get('publishedAt')[:10])
        listArticles.append(newTuple)
    return listArticles


def processArticlesTuple(listArticles):   
    filename = 'stockArticles2.csv'
    with open(filename, 'a') as f:
        w = csv.DictWriter(f, file_utils.FIELDS)
        w.writeheader()
        for article in listArticles:     
            w.writerow(dict(article._asdict()))
