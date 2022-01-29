import os.path
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os.path
from django.utils import timezone
from django.db import models


class StockSymbol(models.Model):
    name = models.CharField(unique=True, max_length=10)
    user_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def getStocks(self):
        #stocks = getStockSymbols(get_top_25_gainers_chart())
        print(stocks)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_stock_ticker')]
        ordering=['name']


class PriceData(models.Model):
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateField(default=datetime(1800, 1, 1))
    open = models.DecimalField(decimal_places=4, max_digits=20, null=True)
    close = models.DecimalField(decimal_places=4, max_digits=20, null=True)
    volume = models.BigIntegerField(null=True)

    def __str__(self):
        template = '{0.stock} {0.date} {0.close}'
        return template.format(self)
    
    class Meta: 
        constraints = [models.UniqueConstraint(fields=['stock', 'date'], name='unique_price_data')]
        ordering=['-date']


class StockArticle(models.Model):
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateField()
    sentiment = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    scraper = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        template = '{0.stock} {0.name} {0.date}'
        return template.format(self)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['stock', 'date', 'name'], name='unique_article')]
        ordering=['-date']


class StockLoser(models.Model):
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateTimeField()
    change_percentage = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    trade_volume = models.BigIntegerField(null=True)
    avg_3_month_volume = models.BigIntegerField(null=True)

    def __str__(self):
        template = '{0.stock} {0.date} {0.change_percentage}'
        return template.format(self)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['stock', 'date'], name='unique_losing_stock')]
        ordering = ['-date', 'change_percentage']


class StockGainer(models.Model):
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    date = models.DateTimeField()
    change_percentage = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    trade_volume = models.BigIntegerField(null=True)
    avg_3_month_volume = models.BigIntegerField(null=True)

    def __str__(self):
        template = '{0.stock} {0.date} {0.change_percentage}'
        return template.format(self)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['stock', 'date'], name='unique_gaining_stock')]
        ordering = ['-date', '-change_percentage']
