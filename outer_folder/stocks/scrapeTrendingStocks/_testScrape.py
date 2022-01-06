import requests
from bs4 import BeautifulSoup
import re

def get_price(tableRowString):
    price = (re.search('Price \(Intraday\)[\s\S]*?(?=<\/)', tableRowString)).group()
    print(price)
    price = (re.search('>[0-9][,.0-9]*', price)).group()
    print(price)
    price = price[1:]

    return price


gainURL = 'https://finance.yahoo.com/gainers?offset=0&count=100'

gainRequest = requests.get(gainURL)

soupGain = BeautifulSoup(gainRequest.content, 'html.parser')

gainTable = soupGain.findAll('tr', attrs = {'class':'simpTblRow'})

for i in gainTable:
    print(get_price(str(i)))
