from flask import Flask, render_template, url_for, request, redirect, abort, flash, jsonify, session, make_response, json
import sqlite3
import pandas as pd
import plotly
import plotly.express as px
import sys
sys.path.append('..')
from utils import sqlite_utils
from scrapeTrendingStocks import y_scrape_utils




app = Flask(__name__)

selectedStock = []

@app.route('/', methods = ['GET', 'POST'])
def index():
    errors = []
    graphSelect = None
    #selectedStock = []

    gainerConn = sqlite_utils.createConnection("/var/stockSA/stockGainers.db")


    #multiStockGainers = sqlite_utils.findMultipleStockGainers(gainerConn)
    query = 'SELECT stockSymbol, COUNT(*) FROM stockGainers GROUP BY stockSymbol HAVING COUNT(*) > 1 ORDER BY COUNT(*) DESC';
    multiStockGainers = pd.read_sql(query, gainerConn)

    # multiGainers graph

    fig2 = px.bar(multiStockGainers, y='COUNT(*)', x='stockSymbol', title='Multi Gainers', labels = {'stockSymbol': 'Stock Ticker', 'COUNT(*)': 'Total Count'})
    plot_json2 = json.dumps(fig2, cls = plotly.utils.PlotlyJSONEncoder)


    # gainScrape Data

    gainData = y_scrape_utils.getTop25GainingStockForPandasChart()
    gainDf=pd.DataFrame(gainData, columns=['Stock_Ticker', 'Change_Percentage', 'Trade_Volume', 'Avg_3_Month_Volume', 'Price'])

    # graph for scraped Gainers

    fig = px.bar(gainDf, y='Change_Percentage', x='Stock_Ticker', title='Stock Gainers', labels = {'Stock_Ticker': 'Stock Ticker', 'Change_Percentage': 'Change Percentage'}, text = 'Price')
    plot_json = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)

    #gainer_name fills the drop down select for gainers
    gainer_name = gainData['Stock_Ticker']

    # POST Requests to '/'
    if request.method == 'POST':
        if "gainer" in request.form:
            try:

                selectedStock.extend(request.form.getlist('gainer'))
                print(selectedStock)

            except:
                errors.append("error")
        elif "graphType" in request.form:
            try:
                graphSelect = request.form.get('graphType')
                print(graphSelect)
            except:
                errors.append("error")


    return render_template("index.html", plot_json = plot_json, plot_json2 = plot_json2, gainer_name = gainer_name, errors = errors, selectedStock = selectedStock, graphSelect = graphSelect)


#def addToSelected():
#    selectedStock.extend(request.form.getlist('gainer'))




if __name__ == "__main__":
    app.run(debug=True)
