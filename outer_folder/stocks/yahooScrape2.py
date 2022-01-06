import sys
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime 


top_25_gainers_url = 'https://finance.yahoo.com/gainers'

def get_top_25_gainers_chart():
    top_25_gainers_url = 'https://finance.yahoo.com/gainers'
    gainers_request = requests.get(top_25_gainers_url)
    soup_gainers= BeautifulSoup(gainers_request.content, 'html.parser')
    gainers_table = soup_gainers.findAll('tr', attrs = {'class':'simpTblRow'})

    return gainers_table

def getStockSymbols(table):
    tickers = []
    for tr in table:
        td = tr.find_all('td')
        tickers.append(td[0].text)
    
    return tickers



def parse_table(table):
    for tr in table: 
        td = tr.find_all('td')
        ticker = td[0].text
        price = float(td[2].text.replace(',',''))
        trade_volume = adapt_trade_volume(td[5].text)
        change_percentage = adapt_change_percentage(td[4].text) # needs to be adapted 
        avg_3_month_volume = adapt_trade_volume(td[6].text) # needs to be adapted
        date = get_todays_date_with_hour()
        print(ticker, price, trade_volume, change_percentage, avg_3_month_volume, date)

        save_stock_name(ticker)

        # need to adapt data

        # need to send data to custom save 
    
    return

def save_stock_name(ticker):
    current_tickers = StockSymbol.objects.all()

    if not StockSymbol.objects.filter(name=ticker):
        StockSymbol.objects.create(ticker)



# Neeed function that checks if stockSymbol is in table yet, if not, creates it 



# for date see helper functions 
def get_todays_date_with_hour():
    """
    This function gets todays date with hour
    Returns:
        reformatedDate in the form: "YYYY-MM-DD HH"
    """
    date= datetime.today()
    reformatedDate= ( str(date.year) + "-" + str(date.month) + "-" +
                      str(date.day) + " " + str(date.hour) )
    return reformatedDate

# for trade volume and avg 3 month volume see adaptTradeVolume 
def adapt_trade_volume(tradeVolume):
    """ This function takes the trade volume string from
    our scraper and turns it into an int, formatting correctly
    for our database, removing commas and multiplying out
    data with an 'M' designated for million
    """

    formatted_trade_volume = tradeVolume

    # removing any commas
    formatted_trade_volume = formatted_trade_volume.replace(',','')

    # multiplying out if the string designated has an M
    if formatted_trade_volume[-1] == 'M':
        formatted_trade_volume = float(formatted_trade_volume[:-1])
        # multiply decimal by 1 million for conversion
        formatted_trade_volume = formatted_trade_volume * 1000000

    # converting to an int
    formatted_trade_volume = int(formatted_trade_volume)
    return formatted_trade_volume

def adapt_change_percentage(percent):
    if percent[0]=='+':
        percentage = float(percent[1:-1])/100
    elif percent[0]=='-':
        percentage = float(percent[1:-1])/-100
    else:
        percentage = float(percent[:-1])/100
    return percentage


# Test 

#table = get_top_25_gainers_chart(top_25_gainers_url)

#parse_table(table)
