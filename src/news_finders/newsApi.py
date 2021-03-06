
import requests
from utils import helper_functions


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
