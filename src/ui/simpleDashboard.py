import sys
sys.path.append('..')
from scrapeTrendingStocks import y_scrape_utils
import streamlit as st
import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt



st.set_page_config(layout="wide")

#st.title("Dashboard for Stock Sentiment Analysis Project")
st.markdown("<h1 style='text-align: center; color: green;'>Dashboard for Stock Sentiment Analysis Project</h1>", unsafe_allow_html=True)

expander = st.beta_expander('About')
expander.write("UI built to display today's top gaining stocks, top losing stocks, and top traded. Below, you can query article data for selected/ input stock and the sentiment of those stock. Continuing to add additional comparisons and charts")

# basic structure to get somewhat centered buttons
col1, col2, col3, col4, col5, col6, col7 = st.beta_columns(7)

# buttons for queries
getTop25 = col3.button('Lookup Top 25 Stocks in Each Category')
getTop100 = col5.button('Lookup Top 100 Stocks in Each Category')

# setting up our 3 categories into columns for the scraper
gain, loss, volume = st.beta_columns(3)

gain.subheader('Top Gainers')
loss.subheader('Top Losers')
volume.subheader('Top Trade Volume')

# creating variables for mutliselects (for user to search article and historical stock data on)
gainData = y_scrape_utils.getTop25GainingStockForPandasChart()
topGainers = gainData['Stock_Ticker']

lossData = y_scrape_utils.getTop25LosingStockForPandasChart()
topLosers = lossData['Stock_Ticker']

totTradeData = y_scrape_utils.getTop25MostTradedStockForPandasChart()
topTraded = totTradeData["Stock_Ticker"]

if getTop25:

    # Gains
    gainData = y_scrape_utils.getTop25GainingStockForPandasChart()
    gainDf=pd.DataFrame(gainData, columns=['Stock_Ticker', 'Change_Percentage', 'Trade_Volume', 'Avg_3_Month_Volume'])
    gain.write(gainDf)

    # Gain Graphing Setup
    gainStocks = gainData['Stock_Ticker']
    Gains = gainData['Change_Percentage']

    Gains = [string.strip('%').replace(',','') for string in Gains]
    # Convert Gain Mulitplier to a Float
    Gains = [float(string) for string in Gains]

    gainChart = pd.DataFrame()
    gainChart['Stock Symbols'] = gainStocks
    gainChart['Change %'] = Gains

    chartGain = alt.Chart(gainChart).mark_bar().encode(
    x='Stock Symbols', y = 'Change %')
    gain.altair_chart(chartGain, use_container_width =True)

    # Losses
    lossData = y_scrape_utils.getTop25LosingStockForPandasChart()
    lossDf=pd.DataFrame(lossData, columns=['Stock_Ticker', 'Change_Percentage', 'Trade_Volume', 'Avg_3_Month_Volume'])
    loss.write(lossDf)

    # Loss Graphing Setup
    lossStocks = lossData['Stock_Ticker']
    Losses = lossData['Change_Percentage']

    Losses = [string.strip('%').replace(',','') for string in Losses]
    # Convert Gain Mulitplier to a Float
    Losses = [float(string) for string in Losses]

    lossChart = pd.DataFrame()
    lossChart['Stock Symbols'] = lossStocks
    lossChart['Change %'] = Losses

    chartLoss = alt.Chart(lossChart).mark_bar().encode(
    x='Stock Symbols', y = 'Change %')
    loss.altair_chart(chartLoss, use_container_width =True)

    # Trade Volume Data
    totTradeData = y_scrape_utils.getTop25MostTradedStockForPandasChart()
    totTradeDf=pd.DataFrame(totTradeData, columns=['Stock_Ticker', 'Change_Percentage', 'Trade_Volume', 'Avg_3_Month_Volume'])
    volume.write(totTradeDf)

    # Trade Volume Graph Info



if getTop100:

    # Gains
    gainData = y_scrape_utils.getTop100GainingStockForPandasChart()
    gainDf=pd.DataFrame(gainData, columns=['Stock_Ticker', 'Change_Percentage', 'Trade_Volume', 'Avg_3_Month_Volume'])
    gain.write(gainDf)

    # Gain Graphing Setup
    gainStocks = gainData['Stock_Ticker']
    Gains = gainData['Change_Percentage']

    Gains = [string.strip('%').replace(',','') for string in Gains]
    # Convert Gain Mulitplier to a Float
    Gains = [float(string) for string in Gains]

    gainChart = pd.DataFrame()
    gainChart['Stock Symbols'] = gainStocks
    gainChart['Change %'] = Gains

    chartGain = alt.Chart(gainChart).mark_bar().encode(
    x='Stock Symbols', y = 'Change %')
    gain.altair_chart(chartGain, use_container_width =True)

    # Losses
    lossData = y_scrape_utils.getTop100LosingStockForPandasChart()
    lossDf=pd.DataFrame(lossData, columns=['Stock_Ticker', 'Change_Percentage', 'Trade_Volume', 'Avg_3_Month_Volume'])
    loss.write(lossDf)

    # Loss Graphing Setup
    lossStocks = lossData['Stock_Ticker']
    Losses = lossData['Change_Percentage']

    Losses = [string.strip('%').replace(',','') for string in Losses]
    # Convert Gain Mulitplier to a Float
    Losses = [float(string) for string in Losses]

    lossChart = pd.DataFrame()
    lossChart['Stock Symbols'] = lossStocks
    lossChart['Change %'] = Losses

    chartLoss = alt.Chart(lossChart).mark_bar().encode(
    x='Stock Symbols', y = 'Change %')
    loss.altair_chart(chartLoss, use_container_width =True)

    # Trade Volume Data
    totTradeData = y_scrape_utils.getTop100MostTradedStockForPandasChart()
    totTradeDf=pd.DataFrame(totTradeData, columns=['Stock_Ticker', 'Change_Percentage', 'Trade_Volume', 'Avg_3_Month_Volume'])
    volume.write(totTradeDf)

    # Trade Volume Graph Info

stocksToQuery = []

colGain, colLoss, colVolume = st.beta_columns(3)
selectedGainers = colGain.multiselect('Select Top Gainers to Query', topGainers)
selectedLosers = colLoss.multiselect('Select Top Losers to Query', topLosers)

if selectedGainers:
    stocksToQuery.extend(selectedGainers)
    colGain.write(stocksToQuery)

if selectedLosers:
    stocksToQuery.extend(selectedLosers)
    colLoss.write(stocksToQuery)
# Added

#--------------------------------------------------------------#
## Section Articles
# Pull Database Articles Per Stock

#--------------------------------------------------------------#
## Section Historical Stock Price Data
# Pull Stock
