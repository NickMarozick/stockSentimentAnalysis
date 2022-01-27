from celery import shared_task
from stocks.todays_movers import scrape_losers, scrape_gainers
from .models import StockLoser, StockSymbol, StockGainer
from datetime import datetime

@shared_task(name="say_hello")
def hello(x):
    return "Hello " + x

@shared_task(name="scrape_mover_info")
def scrape():
    scrape_losers()
    scrape_gainers()
    return