
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
articles.appedn(article)

# 2. get content per article


news_scraper = content_scraper.NewsUrlContentScraper()
urls = ['https://www.cnn.com/2019/12/10/media/netflix-stock-sell/index.html']
for url in urls:
    content = news_scraper.getArticleContent(url)
    print(content)
    print('=============\n\n')
    keywords = news_scraper.getArticleKeywords(url)
    print(keywords)
    print('=============\n\n')
    summary = news_scraper.getArticleSummary(url)
    print(summary)


# 3. write to file
for article in articles:
    file_utils.SaveArticleDetailsToFile(article)

