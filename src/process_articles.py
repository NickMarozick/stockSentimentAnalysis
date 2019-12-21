
from news_finders import content_scraper
# from news_finder import NewsAPI_pull_Netflix
from utils import file_utils

STOCKS = []


# 1. get articles
articles = []
name, url, content, description, scraper = foo()
article = file_utils.createArticle(name, url, content, description, scraper)
# dict: article['name'] or article.get('name')
# namedtuple: article.name
article.scraper = 'newsapi'
articles.append(article)


# 2. get content per article
#urls = ['https://www.cnn.com/2019/12/10/media/netflix-stock-sell/index.html']
#for url in urls:
news_scraper = content_scraper.NewsUrlContentScraper()
for article in articles:
    content = news_scraper.getArticleContent(article.url)
    print(content)
    # copy article namedtuple
    article.scraper = 'content_scraper'
    article.content = content
    print('=============\n\n')
    keywords = news_scraper.getArticleKeywords(article.url)
    print(keywords)
    print('=============\n\n')
    summary = news_scraper.getArticleSummary(article.url)
    print(summary)


# 3. write to file
for article in articles:
file_utils.SaveArticleDetailsToFile(article)

