import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils import timezone
from django.conf import settings 
from django.db import models
from .models import StockLoser, StockSymbol, StockGainer
import stocks.utils as utils


def scrape_gainers():
    gainers_table, type = get_top_25_gainers_chart()
    parse_and_save_table(gainers_table, type)
    print("Finished scraping gainers\n")
    return

def scrape_losers():
    losers_table, type = get_top_25_losers_chart()
    parse_and_save_table(losers_table, type)
    print("Finished scraping losers\n")
    return

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
    valid = utils.is_valid_stock_symbol(ticker)

    if valid:
        try:
            id = StockSymbol.objects.get(name=ticker).id
            return id
        except:
            try: 
                app = StockSymbol.objects.create(name=ticker, user_selected=False)
                return app.id
            except Exception as e:
                print('save failed: ', e)
            return
    else:
        print("Invalid Stock Symbol: %s" % ticker)
        return

def parse_and_save_table(table, table_type):

    tz_now = timezone.now().replace(minute=0, second=0, microsecond=0)
    if table_type=="gainers":
        for tr in table: 
            td = tr.find_all('td')
            ticker = td[0].text
            stock_price = float(td[2].text.replace(',',''))
            volume = adapt_trade_volume(td[5].text)
            change_percent = adapt_change_percentage(td[4].text) 
            avg_volume = adapt_trade_volume(td[6].text) 
            
            try: 
                id = get_or_save_stock_symbol_id(ticker)
                print(id)
                StockGainer.objects.create(stock_id=id, date=tz_now, change_percentage=change_percent, price=stock_price, trade_volume=volume, avg_3_month_volume=avg_volume)
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

            try: 
                id = get_or_save_stock_symbol_id(ticker)
                print(id)
                StockLoser.objects.create(stock_id=id, date=tz_now, change_percentage=change_percent, price=stock_price, trade_volume=volume, avg_3_month_volume=avg_volume)
            except Exception as e:
                print("Could not store Stock Gainer %s: %s" %(ticker, e))
        print("Finished saving stock losers\n")
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