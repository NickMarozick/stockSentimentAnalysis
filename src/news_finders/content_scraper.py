
import newspaper

class NewsUrlContentScraper():
    def __init__(self):
        self._article = None

    def _getArticle(self, url):
        try:
            self._article = newspaper.Article(url)
            self._article.download()
            self._article.parse()
        except Exception as e:
            print('Error parsing articles: %s'.format(str(e)))

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

