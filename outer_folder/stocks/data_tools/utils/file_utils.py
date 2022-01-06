#import collections 
import csv
import recordtype


FIELDS = ['stockSymbol', 'name', 'url', 'content', 'description', 'scraper', 'date']
#Article = collections.namedtuple('Article', FIELDS)
Article = recordtype.recordtype('Article', FIELDS)

def createArticle(*FIELDS):
    return Article(*FIELDS)


def saveArticleDetailsToFile(listArticles):
    filename = 'stockArticles2.csv'
    try:
        with open(filename, 'a') as f:
            w = csv.DictWriter(f, FIELDS)
            w.writeheader()
            for article in listArticles:
                w.writerow(dict(article._asdict()))
    except Exception as e: 
        print('Error saving articles to file: {}'.format(str(e)))

