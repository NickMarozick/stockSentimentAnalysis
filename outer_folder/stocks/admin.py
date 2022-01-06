from django.contrib import admin

from .models import StockSymbol, StockArticle, StockLoser, StockGainer, PriceData
# Register your models here.
admin.site.register([StockGainer, StockArticle, StockLoser, PriceData, StockSymbol])