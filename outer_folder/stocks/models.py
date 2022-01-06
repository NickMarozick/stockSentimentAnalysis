import sys
import re
import requests
from bs4 import BeautifulSoup
import os.path
from django.db import models
from django.db.models.constraints import UniqueConstraint
from .yahooScrape2 import getStockSymbols, get_top_25_gainers_chart

# Create your models here.

class StockSymbol(models.Model):
    name = models.CharField(max_length=10)

    UniqueConstraint(fields=['name'], name='unique_stock_ticker')

    def __str__(self):
        return self.name
    
    def getStocks(self):
        stocks = getStockSymbols(get_top_25_gainers_chart())
        print(stocks)

class PriceData(models.Model):
    stock_id = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateField
    low = models.DecimalField
    high = models.DecimalField
    volume = models.BigIntegerField

    UniqueConstraint(fields=['stock_id', 'date'], name='unique_price_data')

    def __str__(self):
        return self.low


class StockArticle(models.Model):
    stock_id = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateField
    sentiment = models.DecimalField
    name = models.CharField
    url = models.URLField
    content = models.TextField
    description = models.TextField
    scraper = models.CharField

    UniqueConstraint(fields=['stock_id', 'date', 'name'], name='unique_article')

    def __str__(self):
        return self.StockArticle_text


class StockLoser(models.Model):
    stock_id = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateField
    change_percentage = models.DecimalField
    price = models.DecimalField
    trade_volume = models.BigIntegerField
    avg_3_month_volume = models.BigIntegerField

    UniqueConstraint(fields=['stock_id', 'date'], name='unique_losing_stock')


class StockGainer(models.Model):
    stock_id = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateField
    change_percentage = models.DecimalField
    price = models.DecimalField
    trade_volume = models.BigIntegerField
    avg_3_month_volume = models.BigIntegerField

    UniqueConstraint(fields=['stock_id', 'date'], name='unique_gaining_stock')

    




# considering stockSymbol model - just pk and stockSymbol --> all others reference and add to 