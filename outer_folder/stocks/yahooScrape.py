import requests
from bs4 import BeautifulSoup
import y_scrape_utils


# setting up our URLs to scrape
mostActiveURL = "https://finance.yahoo.com/most-active?offset=0&count=100"
lossURL = "https://finance.yahoo.com/losers?offset=0&count=100"
gainURL = 'https://finance.yahoo.com/gainers?offset=0&count=100'

# getting content
mostActiveRequest = requests.get(mostActiveURL)
lossRequest = requests.get(lossURL)
gainRequest = requests.get(gainURL)

# parsing content via beautifulSoup
soupMostActive = BeautifulSoup(mostActiveRequest.content, 'html.parser')
soupLoss = BeautifulSoup(lossRequest.content, 'html.parser')
soupGain = BeautifulSoup(gainRequest.content, 'html.parser')

# initiating our dictionaries for the results
mostActiveStocks = {}
losingStocks = {}
gainingStocks = {}

# gathering chart content
mostActiveTable = soupMostActive.findAll('tr', attrs = {'class':'simpTblRow'})
lossTable = soupLoss.findAll('tr', attrs = {'class':'simpTblRow'})
gainTable = soupGain.findAll('tr', attrs = {'class':'simpTblRow'})

#print(mostActiveTable)

for tr in mostActiveTable:
    td = tr.find_all('td')
    row = [i.text for i in td]
    #print(row)
    #print(td[0].text, td[1].text, td[2].text)
    ticker = td[0].text
    tradeVolume = td[5].text # need to adjust 
    changePercentage = td[4].text 
    avg3MonthVolume = td[6].text
    print(ticker, tradeVolume, changePercentage, avg3MonthVolume)
    print(type(ticker))

# iterating and utilizing the regex functions to pull data
# for i in mostActiveTable:
#     ticker = y_scrape_utils.get_ticker(str(i))
#     tradeVolume = y_scrape_utils.get_trade_volume(str(i))
#     changePercentage = y_scrape_utils.get_change_percentage(str(i))
#     avg3MonthVolume = y_scrape_utils.get_avg_3_month_volume(str(i))
#     mostActiveStocks[ticker] = changePercentage, tradeVolume, avg3MonthVolume


# for j in lossTable:
#     ticker = y_scrape_utils.get_ticker(str(j))
#     tradeVolume = y_scrape_utils.get_trade_volume(str(j))
#     changePercentage = y_scrape_utils.get_change_percentage(str(j))
#     avg3MonthVolume = y_scrape_utils.get_avg_3_month_volume(str(j))
#     losingStocks[ticker] = changePercentage, tradeVolume, avg3MonthVolume

# for k in gainTable:
#     ticker = y_scrape_utils.get_ticker(str(k))
#     tradeVolume = y_scrape_utils.get_trade_volume(str(k))
#     changePercentage = y_scrape_utils.get_change_percentage(str(k))
#     avg3MonthVolume = y_scrape_utils.get_avg_3_month_volume(str(k))
#     gainingStocks[ticker] = changePercentage, tradeVolume, avg3MonthVolume


#print("Most Active Stocks: ", mostActiveStocks)
#print("\n")
#print("Losing Stocks: ", losingStocks)
#print("\n")
#print("Gaining Stocks: ", gainingStocks)
#print("\n")
print(gainingStocks)
