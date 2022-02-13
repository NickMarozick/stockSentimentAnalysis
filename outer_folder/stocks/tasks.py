from celery import shared_task
from stocks.todays_movers import scrape_losers, scrape_gainers
from stocks.get_stock_articles import get_and_store_articles_for_stocks
from .models import StockLoser, StockSymbol, StockGainer, StockArticle
from datetime import datetime

user_selected = StockSymbol.objects.filter(user_selected=True).values_list('name', flat=True)

@shared_task(name="say_hello")
def hello(x):
    return "Hello " + x

@shared_task(name="scrape_mover_info")
def scrape():
    scrape_losers()
    scrape_gainers()
    return

@shared_task(name="scrape_articles_for_selected_stock")
def scrape_articles_for_select_stock():
    get_and_store_articles_for_stocks(user_selected)
    return
