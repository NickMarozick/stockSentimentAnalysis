import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from datetime import datetime
from django.conf import settings 
from django.db import models
from .models import StockLoser, StockSymbol, StockGainer


def get_top_25_gainers_chart():
    top_25_gainers_url = 'https://finance.yahoo.com/gainers'
    gainers_request = requests.get(top_25_gainers_url)
    soup_gainers= BeautifulSoup(gainers_request.content, 'html.parser')
    gainers_table = soup_gainers.findAll('tr', attrs = {'class':'simpTblRow'})
    return gainers_table, "gainers"

def get_top_25_losers_chart():
    top_25_losers_url = 'https://finance.yahoo.com/losers'
    losers_request = requests.get(top_25_losers_url)
    soup_losers= BeautifulSoup(losers_request.content, 'html.parser')
    losers_table = soup_losers.findAll('tr', attrs = {'class':'simpTblRow'})
    return losers_table, "losers"

def get_or_save_stock_symbol_id(ticker):
    try:
        id = StockSymbol.objects.get(name=ticker).value('id')
        return id
    except:
        try: 
            app = StockSymbol.objects.create(name=ticker)
            return app.id
        except Exception as e:
            print('save failed: ', e)
        return 

def parse_and_save_table(table, table_type):
    if table_type=="gainer":
        for tr in table: 
            td = tr.find_all('td')
            ticker = td[0].text
            stock_price = float(td[2].text.replace(',',''))
            volume = adapt_trade_volume(td[5].text)
            change_percent = adapt_change_percentage(td[4].text) 
            avg_volume = adapt_trade_volume(td[6].text) 
            scrape_date = datetime.now()
            scrape_date = datetime(scrape_date.year, scrape_date.month, scrape_date.day, scrape_date.hour)

            try: 
                id = get_or_save_stock_symbol_id(ticker)
                print(id)
                stock = StockGainer.objects.create(stock_id=id)
                StockGainer.objects.create(stock_id=id, date=scrape_date, change_percentage=change_percent, price=stock_price, trade_volume=volume, avg_3_month_volume=avg_volume)
            except Exception as e:
                print("Could not store Stock Gainer %s: %s" %(ticker, e))
        print("Finished saving stock gainers\n")
        return 

    elif table_type=='losers':
        for tr in table: 
            td = tr.find_all('td')
            ticker = td[0].text
            stock_price = float(td[2].text.replace(',',''))
            volume = adapt_trade_volume(td[5].text)
            change_percent = adapt_change_percentage(td[4].text) 
            avg_volume = adapt_trade_volume(td[6].text) 
            scrape_date = datetime.now()
            scrape_date = datetime(scrape_date.year, scrape_date.month, scrape_date.day, scrape_date.hour)

            try: 
                id = get_or_save_stock_symbol_id(ticker)
                print(id)
                stock = StockLoser.objects.create(stock_id=id)
                StockLoser.objects.create(stock_id=id, date=scrape_date, change_percentage=change_percent, price=stock_price, trade_volume=volume, avg_3_month_volume=avg_volume)
            except Exception as e:
                print("Could not store Stock Gainer %s: %s" %(ticker, e))
        print("Finished saving stock losers\n")
        return 
    
def save_stock_name(ticker):
    current_tickers = StockSymbol.objects.all()

    if not StockSymbol.objects.filter(name=ticker):
        StockSymbol.objects.create(ticker)
    return

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