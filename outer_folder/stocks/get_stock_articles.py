import requests
import recordtype
from datetime import datetime, timedelta
import stocks.utils as utils
from django.db.models import Max
from .models import StockSymbol, StockArticle 

FIELDS = ['stock_symbol', 'name', 'url', 'content', 'description', 'scraper', 'date']

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
            if not date_dict['date__max']:
                return None
            else:
                revised_date = utils.increment_date(date_dict['date__max'])
                revised_date = transform_date_for_article_api(revised_date)
                return revised_date

        except Exception as e:
            print("Error in getting most current article data date: %s" % e)
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
                print('save failed for %s: %s' % (ticker, e))
            return
    else:
        print("Invalid Stock Symbol: %s" % ticker)
        return

def get_and_store_articles_for_stocks(stocks):
    list_articles= []

    date = utils.get_max_date_for_stock_article_api()

    for stock in stocks:
        last_stored_article_date = get_last_date_stored_articles(stock)
        print(last_stored_article_date)

        if not last_stored_article_date:
            print("None is true")
            articles = get_articles_for_stock(stock, date)
        else:
            articles = get_articles_for_stock(stock, last_stored_article_date)
        # Fix Later: can be more efficient by passing stock name and list of articles per stock to function
        list_articles.extend(articles)
    save_stock_articles(list_articles)

# def get_and_store_articles_for_stocks_with_date(stocks, date):
#     list_articles= []

#     for stock in stocks:
#         last_stored_article_date = get_last_date_stored_articles(stock)
#         print(last_stored_article_date)
#         if last_stored_article_date == None:
#             articles = get_articles_for_stock(stock, date)
#         else:
#             revised_date = utils.increment_date(last_stored_article_date)
#             max_date = utils.get_max_date_for_stock_article_api()
#             # adjusts if prefered article search date is beyond the 28 days allowed by NewsAPI
#             search_from_date = utils.compare_article_dates(revised_date, max_date)
#             articles = get_articles_for_stock(stock, search_from_date)
#         # Fix Later: can be more efficient by passing stock name and list of articles per stock to function
#         list_articles.extend(articles)
#     save_stock_articles(list_articles)

def save_stock_article(article):
    id = get_or_save_stock_symbol_id(article.stock_symbol)
    try:
        StockArticle.objects.create(stock_id=id, name=article.name, url=article.url, content=article.content, description=article.description, date=article.date, scraper=article.scraper)
    except Exception as e:
        #print("could not save article named %s for %s stock\n" % (article.name, article.stock_symbol))
        #print("Error: ", e)
        return
    return 

def save_stock_articles(list_articles):
    for article in list_articles:
        try:
            save_stock_article(article)
        except Exception as e:
            #print("Could not print stock article: %s\n" , article.name)
            #print("Error: ", e)
            return
    return

def get_articles_for_stock(stock_symbol, date):
    url_pattern = ('https://newsapi.org/v2/everything?'
        'q={0}+stock&'
        'from={1}&'
        'sortBy=popularity&'
        'apiKey=ec07e0116ce8450c8b677e877b2e8761')
    url= url_pattern.format(stock_symbol, date)
    response = requests.get(url)
    # using headers could be an area to throttle down as needed, if too many requests
    #headers = response.headers
    #remaining_daily_calls, refresh_date = headers['x-cache-remaining'], headers['x-cache-expires']
    # can use remaining daily calls and refresh date later for throttling down automated cron jobs
    response = response.json()

    if response["status"]=="error":
        print(response["message"])
        exit()

    listArticles= []
    for article in response["articles"]:
        newTuple= create_article(
            stock_symbol, article.get('title'), article.get('url'),
            article.get('content'), article.get('description'),
            "NewsAPI", article.get('publishedAt')[:10])
        listArticles.append(newTuple)
    return listArticles

def create_article(*FIELDS):
    return Article(*FIELDS)
