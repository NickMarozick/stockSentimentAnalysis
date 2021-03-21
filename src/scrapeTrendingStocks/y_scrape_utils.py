import re


def get_ticker(tableRowString):
    ticker = re.search('href="\/quote\/([A-Z-]*)\?p=([A-Z-]*)"', tableRowString)
    ticker = ticker.group()
    ticker = (re.search('\/[A-Z-]*\?', ticker)).group()
    ticker = ticker[1:len(ticker)-1]

    return ticker

def get_trade_volume(tableRowString):
    #tradeVolume = re.search('[0-9.]*M<\/span><\/td><td aria-label="Avg Vol \(3 month\)', tableRowString)
    tradeVolume = re.search('[0-9.,M]*<\/span><\/td><td aria-label="Avg Vol \(3 month\)', tableRowString)
    tradeVolume = tradeVolume.group()
    #tradeVolume = (re.search('[0-9]*.[0-9]*M',tradeVolume)).group()
    tradeVolume = (re.search('[0-9,.M]*',tradeVolume)).group()

    return tradeVolume

def get_change_percentage(tableRowString):
    #print(tableRowString)
    changePercentage = re.search('data-reactid="[0-9]*">([+-][0-9,]*|0)*.[0-9]*%', tableRowString)
    print(changePercentage)
    if changePercentage is None:
        changePercentage = "None"
        print(tableRowString)
        return changePercentage
    changePercentage = changePercentage.group()
    changePercentage = (re.search('([+-][0-9,]*|0)*.[0-9]*%', changePercentage)).group()

    return changePercentage

def get_avg_3_month_volume(tableRowString):
    #avg3MonthVolume= re.search('Avg Vol \(3 month\)" class="Va\(m\) Ta\(end\) Pstart\(20px\) Fz\(s\)" colspan="" data-reactid="[0-9]*"><!-- react-text: [0-9]* -->[0-9]*[.,][0-9M]*', tableRowString)
    avg3MonthVolume= re.search('Avg Vol \(3 month\)" class="Va\(m\) Ta\(end\) Pstart\(20px\) Fz\(s\)" colspan="" data-reactid="[0-9]*"><!-- react-text: [0-9]* -->[0-9.,M]*', tableRowString)
    avg3MonthVolume = avg3MonthVolume.group()
    #avg3MonthVolume= (re.search('>[0-9]*[.,][0-9M]*', avg3MonthVolume)).group()
    avg3MonthVolume= (re.search('-->[0-9.,M]*', avg3MonthVolume)).group()
    avg3MonthVolume= avg3MonthVolume[3:]
    #print(avg3Month)
    return avg3MonthVolume
