import requests
import recordtype
from datetime import datetime, timedelta
import stocks.utils as utils
from .models import StockSymbol, StockArticle 

FIELDS = ['stockSymbol', 'name', 'url', 'content', 'description', 'scraper', 'date']

Article = recordtype.recordtype('Article', FIELDS)

def get_articles_for_stocks(stocks, date):
    listArticles=[]
    for stock in stocks:
        articles = get_articles_for_stock(stock, date)
        listArticles.extend(articles)
    return listArticles

# News API needs date in the form YYYY-MM-DD
def transform_date_for_article_api(date):
    revised_date = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
    return revised_date

def get_last_date_stored_articles(ticker):
    """
    Returns:
        Latest date for article data retrieved (if any)
    """    
    id = get_or_save_stock_symbol_id(ticker)
    if id:
        try:
            date_dict = StockArticle.objects.filter(stock_id=id).aggregate(Max('date'))

            # handles the condition of no date existing for price data 
            if date_dict['date__max'] == None:
                return None
            else:
                revised_date = transform_date_for_article_api(date_dict['date__max'])
                return revised_date

        except Exception as e:
            print("Error in getting most current price data date: %s" % e)
            return 

    else: 
        # condition reached if invalid stock name
        print("Was unable to retrieve or save stock id\n")
        return

def get_or_save_stock_symbol_id(ticker):
    valid = utils.is_valid_stock_symbol(ticker)

    if valid:
        try:
            id = StockSymbol.objects.get(name=ticker).id
            return id
        except:
            try: 
                app = StockSymbol.objects.create(name=ticker)
                return app.id
            except Exception as e:
                print('save failed: ', e)
            return
    else:
        print("Invalid Stock Symbol: %s" % ticker)
        return

def get_and_store_articles_for_stocks(stocks, date):
    list_articles= []

    for stock in stocks:
        last_stored_article_date = get_last_date_stored_articles(stock)
        print(last_stored_article_date)
        if last_stored_article_date == None:
            articles = get_articles_for_stock(stock, date)
        else:
            revised_date = utils.increment_date(last_stored_article_date)
            max_date = utils.get_max_date_for_stock_article_api()
            # adjusts if prefered article search date is beyond the 28 days allowed by NewsAPI
            search_from_date = utils.compare_article_dates(revised_date, max_date)
            articles = get_articles_for_stock(stock, search_from_date)
        # Fix Later: can be more efficient by passing stock name and list of articles per stock to function
        list_articles.extend(articles)
    save_stock_articles(list_articles)

def save_stock_article(article):
    id = get_or_save_stock_symbol_id(article.stockSymbol)
    try:
        StockArticle.create(stock_id=id, name=article.name, url=article.url, content=article.content, description=article.description, date=article.date, scraper=article.scraper)
    #stock, date, sentiment, name, url, content, description, scraper
    except Exception as e:
        print("could not save article named %s for %s stock. Error: %s" % (article.name, article.stockSymbol, e))
    return 

def save_stock_articles(list_articles):
    for article in list_articles:
        try:
            save_stock_article(article)
        except Error as e:
            print("Could not print stock article: %s. Error: %s" (article.name, e))
    return

def get_articles_for_stock(stockSymbol, date):
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
        newTuple= create_article(
            stockSymbol, article.get('title'), article.get('url'),
            article.get('content'), article.get('description'),
            "NewsAPI", article.get('publishedAt')[:10])
        listArticles.append(newTuple)
    return listArticles

def create_article(*FIELDS):
    return Article(*FIELDS)


# Need createArticle 
# need recordType import? 
# import recordtype
# FIELDS = ['stockSymbol', 'name', 'url', 'content', 'description', 'scraper', 'date']

# Article = recordtype.recordtype('Article', FIELDS)

# def createArticle(*FIELDS):
#     return Article(*FIELDS)