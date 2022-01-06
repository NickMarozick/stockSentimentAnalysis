from django.http import HttpResponse
from django.template import loader
#from outer_folder.stocks.models import StockGainer
from .models import StockGainer, StockSymbol

def index(request):
    latest_gainer_list = StockGainer.objects.order_by('stock_id')[:5]
    stock_list = StockSymbol.objects.get(id=1)
    template = loader.get_template('stocks/index.html')
    context = {
        'latest_gainer_list': latest_gainer_list,
        'stock_list': stock_list,
    }
    return HttpResponse(template.render(context, request))
