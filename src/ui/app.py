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

@app.route('/')
def index():
    gainerConn = sqlite_utils.createConnection("/var/stockSA/stockGainers.db")

    multiStockGainers = sqlite_utils.findMultipleStockGainers(gainerConn)
    #print(multiStockGainers)

    gainData = y_scrape_utils.getTop25GainingStockForPandasChart()
    gainDf=pd.DataFrame(gainData, columns=['Stock_Ticker', 'Change_Percentage', 'Trade_Volume', 'Avg_3_Month_Volume'])
    #gain.write(gainDf)

    print(gainDf)

    fig = px.bar(gainDf, y='Change_Percentage', x='Stock_Ticker', title='Stock Gainers')
    #fig.update_yaxes(categoryorder='category ascending')
    plot_json = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", graph1 = multiStockGainers, gain = gainDf, plot_json = plot_json)


if __name__ == "__main__":
    app.run(debug=True)
