import re
import requests
from bs4 import BeautifulSoup
from utils import sqlite_utils


def get_ticker(tableRowString):
    ticker = re.search('href="\/quote\/([A-Z-]*)\?p=([A-Z-]*)"', tableRowString)
    ticker = ticker.group()
    ticker = (re.search('\/[A-Z-]*\?', ticker)).group()
    ticker = ticker[1:len(ticker)-1]

    return ticker

def get_trade_volume(tableRowString):
    tradeVolume = re.search('[0-9.,M]*<\/span><\/td><td aria-label="Avg Vol \(3 month\)', tableRowString)
    tradeVolume = tradeVolume.group()
    tradeVolume = (re.search('[0-9,.M]*',tradeVolume)).group()

    return tradeVolume

def get_change_percentage(tableRowString):
    changePercentage = re.search('data-reactid="[0-9]*">([+-][0-9,]*|0)*.[0-9]*%', tableRowString)
    if changePercentage is None:
        changePercentage = "None"
        return changePercentage
    changePercentage = changePercentage.group()
    changePercentage = (re.search('([+-][0-9,]*|0)*.[0-9]*%', changePercentage)).group()

    return changePercentage

def get_avg_3_month_volume(tableRowString):
    avg3MonthVolume= re.search('Avg Vol \(3 month\)" class="Va\(m\) Ta\(end\) Pstart\(20px\) Fz\(s\)" colspan="" data-reactid="[0-9]*"><!-- react-text: [0-9]* -->[0-9.,M]*', tableRowString)
    avg3MonthVolume = avg3MonthVolume.group()
    avg3MonthVolume= (re.search('-->[0-9.,M]*', avg3MonthVolume)).group()
    avg3MonthVolume= avg3MonthVolume[3:]

    return avg3MonthVolume

def get_price(tableRowString):
    price = (re.search('Price \(Intraday\)[\s\S]*?(?=<\/)', tableRowString)).group()
    price = (re.search('>[0-9][,.0-9]*', price)).group()
    price = price[1:]

    return price

def getTop100GainingStock():
    #setting up the beautifulSoup
    gainURL = 'https://finance.yahoo.com/gainers?offset=0&count=100'
    gainRequest = requests.get(gainURL)
    soupGain = BeautifulSoup(gainRequest.content, 'html.parser')

    # adding our dictionary to return
    gainingStocks = {}

    # finding the specific tableRows
    gainTable = soupGain.findAll('tr', attrs = {'class':'simpTblRow'})

    for k in gainTable:
        ticker = get_ticker(str(k))
        tradeVolume = get_trade_volume(str(k))
        changePercentage = get_change_percentage(str(k))
        avg3MonthVolume = get_avg_3_month_volume(str(k))
        gainingStocks[ticker] = changePercentage, tradeVolume, avg3MonthVolume

    return gainingStocks

def getTop25GainingStock():
    #setting up the beautifulSoup
    gainURL = 'https://finance.yahoo.com/gainers?count=25&offset=0'
    gainRequest = requests.get(gainURL)
    soupGain = BeautifulSoup(gainRequest.content, 'html.parser')

    # adding our dictionary to return
    gainingStocks = {}

    # finding the specific tableRows
    gainTable = soupGain.findAll('tr', attrs = {'class':'simpTblRow'})

    for k in gainTable:
        ticker = get_ticker(str(k))
        tradeVolume = get_trade_volume(str(k))
        changePercentage = get_change_percentage(str(k))
        avg3MonthVolume = get_avg_3_month_volume(str(k))
        gainingStocks[ticker] = changePercentage, tradeVolume, avg3MonthVolume

    return gainingStocks

def getTop100GainingStockForPandasChart():
    #setting up the beautifulSoup
    gainURL = 'https://finance.yahoo.com/gainers?count=100&offset=0'
    gainRequest = requests.get(gainURL)
    soupGain = BeautifulSoup(gainRequest.content, 'html.parser')

    # adding our dictionary to return
    gainingStocks = {'Stock_Ticker': [], 'Trade_Volume': [], 'Change_Percentage': [], 'Avg_3_Month_Volume': []}

    # finding the specific tableRows
    gainTable = soupGain.findAll('tr', attrs = {'class':'simpTblRow'})

    for k in gainTable:
        ticker = get_ticker(str(k))
        tradeVolume = get_trade_volume(str(k))
        changePercentage = get_change_percentage(str(k))
        avg3MonthVolume = get_avg_3_month_volume(str(k))
        #gainingStocks[ticker] = changePercentage, tradeVolume, avg3MonthVolume
        gainingStocks['Stock_Ticker'].append(ticker)
        gainingStocks['Trade_Volume'].append(tradeVolume)
        gainingStocks['Change_Percentage'].append(changePercentage)
        gainingStocks['Avg_3_Month_Volume'].append(avg3MonthVolume)

    return gainingStocks

def getTop25GainingStockForPandasChart():
    #setting up the beautifulSoup
    gainURL = 'https://finance.yahoo.com/gainers?count=25&offset=0'
    gainRequest = requests.get(gainURL)
    soupGain = BeautifulSoup(gainRequest.content, 'html.parser')

    # adding our dictionary to return
    gainingStocks = {'Stock_Ticker': [], 'Trade_Volume': [], 'Change_Percentage': [], 'Avg_3_Month_Volume': [], 'Price': []}

    # finding the specific tableRows
    gainTable = soupGain.findAll('tr', attrs = {'class':'simpTblRow'})

    for k in gainTable:
        ticker = get_ticker(str(k))
        tradeVolume = get_trade_volume(str(k))
        changePercentage = get_change_percentage(str(k))
        changePercentage = changePercentage[1:-1]
        changePercentage = float(changePercentage)
        avg3MonthVolume = get_avg_3_month_volume(str(k))
        price = get_price(str(k))

        gainingStocks['Stock_Ticker'].append(ticker)
        gainingStocks['Trade_Volume'].append(tradeVolume)
        gainingStocks['Change_Percentage'].append(changePercentage)
        gainingStocks['Avg_3_Month_Volume'].append(avg3MonthVolume)
        gainingStocks['Price'].append(price)
    return gainingStocks

def getTop100LosingStockForPandasChart():
    #setting up the beautifulSoup
    lossURL = "https://finance.yahoo.com/losers?offset=0&count=100"
    lossRequest = requests.get(lossURL)
    soupLoss = BeautifulSoup(lossRequest.content, 'html.parser')

    # adding our dictionary to return
    losingStocks = {'Stock_Ticker': [], 'Trade_Volume': [], 'Change_Percentage': [], 'Avg_3_Month_Volume': []}

    # finding the specific tableRows
    lossTable = soupLoss.findAll('tr', attrs = {'class':'simpTblRow'})

    for j in lossTable:
        ticker = get_ticker(str(j))
        tradeVolume = get_trade_volume(str(j))
        changePercentage = get_change_percentage(str(j))
        avg3MonthVolume = get_avg_3_month_volume(str(j))

        losingStocks['Stock_Ticker'].append(ticker)
        losingStocks['Trade_Volume'].append(tradeVolume)
        losingStocks['Change_Percentage'].append(changePercentage)
        losingStocks['Avg_3_Month_Volume'].append(avg3MonthVolume)

    return losingStocks

def getTop25LosingStockForPandasChart():
    #setting up the beautifulSoup
    lossURL = "https://finance.yahoo.com/losers?offset=0&count=25"
    lossRequest = requests.get(lossURL)
    soupLoss = BeautifulSoup(lossRequest.content, 'html.parser')

    # adding our dictionary to return
    losingStocks = {'Stock_Ticker': [], 'Trade_Volume': [], 'Change_Percentage': [], 'Avg_3_Month_Volume': []}

    # finding the specific tableRows
    lossTable = soupLoss.findAll('tr', attrs = {'class':'simpTblRow'})

    for j in lossTable:
        ticker = get_ticker(str(j))
        tradeVolume = get_trade_volume(str(j))
        changePercentage = get_change_percentage(str(j))
        avg3MonthVolume = get_avg_3_month_volume(str(j))

        losingStocks['Stock_Ticker'].append(ticker)
        losingStocks['Trade_Volume'].append(tradeVolume)
        losingStocks['Change_Percentage'].append(changePercentage)
        losingStocks['Avg_3_Month_Volume'].append(avg3MonthVolume)

    return losingStocks

def getTop100LosingStock():
    #setting up the beautifulSoup
    lossURL = "https://finance.yahoo.com/losers?offset=0&count=100"
    lossRequest = requests.get(lossURL)
    soupLoss = BeautifulSoup(lossRequest.content, 'html.parser')

    # adding our dictionary to return
    losingStocks = {}

    # finding the specific tableRows
    lossTable = soupLoss.findAll('tr', attrs = {'class':'simpTblRow'})

    for j in lossTable:
        ticker = get_ticker(str(j))
        tradeVolume = get_trade_volume(str(j))
        changePercentage = get_change_percentage(str(j))
        avg3MonthVolume = get_avg_3_month_volume(str(j))
        losingStocks[ticker] = changePercentage, tradeVolume, avg3MonthVolume

    return losingStocks


def getTop25LosingStock():
    #setting up the beautifulSoup
    lossURL = "https://finance.yahoo.com/losers?offset=0&count=25"
    lossRequest = requests.get(lossURL)
    soupLoss = BeautifulSoup(lossRequest.content, 'html.parser')

    # adding our dictionary to return
    losingStocks = {}

    # finding the specific tableRows
    lossTable = soupLoss.findAll('tr', attrs = {'class':'simpTblRow'})

    for j in lossTable:
        ticker = get_ticker(str(j))
        tradeVolume = get_trade_volume(str(j))
        changePercentage = get_change_percentage(str(j))
        avg3MonthVolume = get_avg_3_month_volume(str(j))
        losingStocks[ticker] = changePercentage, tradeVolume, avg3MonthVolume

    return losingStocks

def getTop100MostTradedStockForPandasChart():
    #setting up the beautifulSoup
    mostActiveURL = "https://finance.yahoo.com/most-active?offset=0&count=100"
    mostActiveRequest = requests.get(mostActiveURL)
    soupMostActive = BeautifulSoup(mostActiveRequest.content, 'html.parser')

    # adding our dictionary to return
    mostActiveStocks = {'Stock_Ticker': [], 'Trade_Volume': [], 'Change_Percentage': [], 'Avg_3_Month_Volume': []}

    # finding the specific tableRows
    mostActiveTable = soupMostActive.findAll('tr', attrs = {'class':'simpTblRow'})

    for i in mostActiveTable:
        ticker = get_ticker(str(i))
        tradeVolume = get_trade_volume(str(i))
        changePercentage = get_change_percentage(str(i))
        avg3MonthVolume = get_avg_3_month_volume(str(i))

        mostActiveStocks['Stock_Ticker'].append(ticker)
        mostActiveStocks['Trade_Volume'].append(tradeVolume)
        mostActiveStocks['Change_Percentage'].append(changePercentage)
        mostActiveStocks['Avg_3_Month_Volume'].append(avg3MonthVolume)

    return mostActiveStocks

def getTop25MostTradedStockForPandasChart():
    #setting up the beautifulSoup
    mostActiveURL = "https://finance.yahoo.com/most-active?offset=0&count=25"
    mostActiveRequest = requests.get(mostActiveURL)
    soupMostActive = BeautifulSoup(mostActiveRequest.content, 'html.parser')

    # adding our dictionary to return
    mostActiveStocks = {'Stock_Ticker': [], 'Trade_Volume': [], 'Change_Percentage': [], 'Avg_3_Month_Volume': []}

    # finding the specific tableRows
    mostActiveTable = soupMostActive.findAll('tr', attrs = {'class':'simpTblRow'})

    for i in mostActiveTable:
        ticker = get_ticker(str(i))
        tradeVolume = get_trade_volume(str(i))
        changePercentage = get_change_percentage(str(i))
        avg3MonthVolume = get_avg_3_month_volume(str(i))

        mostActiveStocks['Stock_Ticker'].append(ticker)
        mostActiveStocks['Trade_Volume'].append(tradeVolume)
        mostActiveStocks['Change_Percentage'].append(changePercentage)
        mostActiveStocks['Avg_3_Month_Volume'].append(avg3MonthVolume)

    return mostActiveStocks

def getTop100MostTradedStock():
    #setting up the beautifulSoup
    mostActiveURL = "https://finance.yahoo.com/most-active?offset=0&count=100"
    mostActiveRequest = requests.get(mostActiveURL)
    soupMostActive = BeautifulSoup(mostActiveRequest.content, 'html.parser')

    # adding our dictionary to return
    mostActiveStocks = {}

    # finding the specific tableRows
    mostActiveTable = soupMostActive.findAll('tr', attrs = {'class':'simpTblRow'})

    for i in mostActiveTable:
        ticker = get_ticker(str(i))
        tradeVolume = get_trade_volume(str(i))
        changePercentage = get_change_percentage(str(i))
        avg3MonthVolume = get_avg_3_month_volume(str(i))
        mostActiveStocks[ticker] = changePercentage, tradeVolume, avg3MonthVolume

    return mostActiveStocks

def getTop25MostTradedStock():
    #setting up the beautifulSoup
    mostActiveURL = "https://finance.yahoo.com/most-active?offset=0&count=25"
    mostActiveRequest = requests.get(mostActiveURL)
    soupMostActive = BeautifulSoup(mostActiveRequest.content, 'html.parser')

    # adding our dictionary to return
    mostActiveStocks = {}

    # finding the specific tableRows
    mostActiveTable = soupMostActive.findAll('tr', attrs = {'class':'simpTblRow'})

    for i in mostActiveTable:
        ticker = get_ticker(str(i))
        tradeVolume = get_trade_volume(str(i))
        changePercentage = get_change_percentage(str(i))
        avg3MonthVolume = get_avg_3_month_volume(str(i))
        mostActiveStocks[ticker] = changePercentage, tradeVolume, avg3MonthVolume

    return mostActiveStocks

def getAndStoreTop25GainingStocks(conn):
    gainers = getTop25GainingStock()

    sqlite_utils._insertGainers(conn, gainers)

def getAndStoreTop25LosingStocks(conn):
    losers = getTop25LosingStock()

    sqlite_utils._insertLosers(conn, losers)
