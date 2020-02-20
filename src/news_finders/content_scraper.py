
import newspaper
from newspaper import Article 
from newspaper import Config

class NewsUrlContentScraper():
    def __init__(self):
        self._article = None

    def _getArticle(self, url):
        try:
            self._article = newspaper.Article(url)
            self._article.download()
            self._article.parse()
        
        except Exception as e: 
            print(e)
            print('Initial error parsing articles')
                
            try:
                user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
                config = Config()
                config.browser_user_agent = user_agent
                self._article = newspaper.Article(url, config=config)
                self._article.download()
                self._article.parse()
    
            except Exception as e:
                print(e)
                if self._article.text=="":
                    print('Error after changing user agent to retrieve article')
                    self._article.text="error"

    def getArticleContent(self, url):
        if self._article is None:
            self._getArticle(url)
        
        if self._article is not None:
            return self._article.text
        else:
            return ''

    def getArticleKeywords(self, url):
        if self._article is None:
            self._getArticle(url)
        
        if self._article is not None:
            return self._article.keywords
        else:
            return []

    def getArticleSummary(self, url):
        if self._article is None:
            self._getArticle(url)
        
        if self._article is not None:
            return self._article.summary
        else:
            return ''

