from django.contrib import admin

from .models import StockSymbol, StockArticle, StockLoser, StockGainer, PriceData
# Register your models here.

class StockSymbolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user_selected')

class StockArticleAdmin(admin.ModelAdmin):
    list_display = ('stock', 'date', 'name', 'sentiment', 'url', 'content', 'description')

class PriceDataAdmin(admin.ModelAdmin):
    list_display = ('stock', 'date', 'open', 'close', 'volume')

class StockGainerAdmin(admin.ModelAdmin):
    list_display = ('stock', 'date', 'change_percentage', 'price', 'trade_volume', 'avg_3_month_volume')

class StockLoserAdmin(admin.ModelAdmin):
    list_display = ('stock', 'date', 'change_percentage', 'price', 'trade_volume', 'avg_3_month_volume')


admin.site.register(StockSymbol, StockSymbolAdmin)

admin.site.register(StockArticle, StockArticleAdmin)

admin.site.register(PriceData, PriceDataAdmin)

admin.site.register(StockGainer, StockGainerAdmin)

admin.site.register(StockLoser, StockLoserAdmin)
