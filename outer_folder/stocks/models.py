import os.path
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os.path
from django.utils import timezone
from django.db import models
from django.db.models.constraints import UniqueConstraint


class StockSymbol(models.Model):
    name = models.CharField(max_length=10)

    UniqueConstraint(fields=['name'], name='unique_stock_ticker')

    def __str__(self):
        return self.name
    
    def getStocks(self):
        #stocks = getStockSymbols(get_top_25_gainers_chart())
        print(stocks)
    

class PriceData(models.Model):
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateField(default=datetime(1800, 1, 1))
    open = models.DecimalField(decimal_places=4, max_digits=20, null=True)
    close = models.DecimalField(decimal_places=4, max_digits=20, null=True)
    volume = models.BigIntegerField(null=True)

    UniqueConstraint(fields=['stock', 'date'], name='unique_price_data')

    def __str__(self):
        return self.stock, self.date, self.close
    
    class Meta: 
        ordering=['-date']


class StockArticle(models.Model):
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateField(default=datetime(1800, 1, 1))
    sentiment = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    scraper = models.CharField(max_length=100, null=True, blank=True)

    UniqueConstraint(fields=['stock', 'date', 'name'], name='unique_article')

    def __str__(self):
        return self.stock, self.name
    
    class Meta:
        ordering=['-date']


class StockLoser(models.Model):
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime(1800, 1, 1))
    change_percentage = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    trade_volume = models.BigIntegerField(null=True)
    avg_3_month_volume = models.BigIntegerField(null=True)

    UniqueConstraint(fields=['stock', 'date'], name='unique_losing_stock')

    def __str__(self):
        return self.stock, self.date, self.change_percentage
    class Meta:
        ordering = ['-date', 'change_percentage']


class StockGainer(models.Model):
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime(1800, 1, 1))
    change_percentage = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    trade_volume = models.BigIntegerField(null=True)
    avg_3_month_volume = models.BigIntegerField(null=True)

    UniqueConstraint(fields=['stock', 'date'], name='unique_gaining_stock')

    def __str__(self):
        return self.stock, self.date, self.change_percentage
    
    class Meta:
        ordering = ['-date', '-change_percentage']
