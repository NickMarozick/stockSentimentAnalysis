#from news_finders import content_scraper

from news_finders import newsApi
from utils import file_utils

#STOCKS = ["AAPL", "ABBV", "ABT", "ACN", "ADBE", "AGN", "AIG", "ALL", "AMGN", "AMZN", "AXP", "BA", "BAC", "BIIB", "BK", "BKNG", "BLK", "BMY", "BRKB", "C", "CAT", "CHTR", "CL", "CMCSA", "COF", "COP", "COST", "CSCO", "CVS", "CVX", "DD", "DHR", "DIS", "DOW", "DUK", "EMR", "EXC", "F", "FB", "FDX", "GD", "GE", "GILD", "GM", "GOOG", "GOOGL", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KHC", "KMI", "KO", "LLY", "LMT", "LOW", "MA", "MCD", "MDLZ", "MDT", "MET", "MMM", "MO", "MRK", "MS", "MSFT", "NEE", "NFLX", "NKE", "NVDA", "ORCL", "OXY", "PEP", "PFE", "PG", "PM", "PYPL", "QCOM", "RTN", "SBUX", "SLB", "SO", "SPG", "T", "TGT", "TMO", "TXN", "UNH", "UNP", "UPS", "USB", "UTX", "V", "VZ", "WBA", "WFC", "WMT", "XOM"]

STOCKS = ["AAPL", "ABBV", "TXN"]


date= '2019-12-19'

articles = []
articles = newsApi.getArticlesForMultipleStocks(STOCKS, date)
newsApi.processArticlesTuple(articles)

#news_scraper = content_scraper.NewsUrlContentScraper()
#for article in articles:
#    content = news_scraper.getArticleContent(article.url)
#    print(content)
    # copy article namedtuple
#    article.scraper = 'content_scraper'
#    article.content = content
#    print('=============\n\n')
#    keywords = news_scraper.getArticleKeywords(article.url)
#    print(keywords)
#    print('=============\n\n')
#    summary = news_scraper.getArticleSummary(article.url)
#    print(summary)



