from yahoofinancials import YahooFinancials

ticker= 'AAPL'

yahoo_financials = YahooFinancials(ticker)

#dateRange = []

dateRange = yahoo_financials.get_historical_price_data("2020-06-09", "2020-07-08", "daily")

#print(dateRange.price)

#print(yahoo_financials.get_historical_price_data("2020-06-09", "2020-07-08", "daily"))

#print(dateRange)

#for i in dateRange:
#    print(i, dateRange[i])


#for date in dateRange:
#    print(date.prices.low)

historicalStockPrices=yahoo_financials.get_historical_price_data("2020-06-09", "2020-07-08", "daily")

prices=historicalStockPrices['AAPL']['prices']

for price in prices:
    date=price['formatted_date']
    low=price['low']
    high=price['high']
    opening=price['open']
    close=price['close']
    volume=price['volume']
    print(date, low, high, opening, close, volume)
