import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.offline import plot
import json
from django.http import HttpResponse
from django.template import loader
#from outer_folder.stocks.models import StockGainer
from .models import StockGainer, StockSymbol, StockLoser

def index(request):
    latest_gainer_list = StockGainer.objects.order_by('stock_id')[:5]
    stock_list = StockSymbol.objects.get(id=1)


    template = loader.get_template('stocks/index.html')
    losers_queryset = StockLoser.objects.values_list('stock__name', 'date', 'change_percentage', 'price', 'trade_volume')
    gainers_queryset = StockGainer.objects.values_list('stock__name', 'date', 'change_percentage', 'price', 'trade_volume')
    gain_df= pd.DataFrame(list(gainers_queryset), columns=['stock', 'date', 'change_percentage', 'price', 'trade_volume'])
    loss_df= pd.DataFrame(list(losers_queryset), columns=['stock', 'date', 'change_percentage', 'price', 'trade_volume'])
    gainer_fig = px.bar(gain_df, y='change_percentage', x='stock', title='Stock Gainers', labels = {'stock': 'Stock Ticker', 'change_percentage': 'Change Percentage'}, text = ["$ " + str(elem) for elem in gain_df['price']])
    loss_fig = px.bar(loss_df, y='change_percentage', x='stock', title='Stock Losers', labels = {'stock': 'Stock Ticker', 'change_percentage': 'Change Percentage'}, text = ["$ " + str(elem) for elem in loss_df['price']])
    gainer_fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    loss_fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    gainer_div = plot(gainer_fig, auto_open=False, output_type="div")
    loss_div = plot(loss_fig, auto_open=False, output_type="div")
    context = {
        'latest_gainer_list': latest_gainer_list,
        'stock_list': stock_list,
        'gain_df': gain_df,
        'gainer_graph_div': gainer_div,
        'loss_graph_div': loss_div,
    }
    return HttpResponse(template.render(context, request))
