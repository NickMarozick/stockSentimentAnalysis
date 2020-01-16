#import collections 
import csv
import recordtype


FIELDS = ['stockSymbol', 'name', 'url', 'content', 'description', 'scraper', 'date']
#Article = collections.namedtuple('Article', FIELDS)
Article = recordtype.recordtype('Article', FIELDS)

def createArticle(*FIELDS):
    return Article(*FIELDS)


def saveArticleDetailsToFile(article):
    filename = 'stockNewsArticles.csv'
    try:
        with open(filename, 'a') as f:      # open file in append mode
            csv_writer = csv.DictWriter(f, FIELDS)
            csv_writer.writeheader()
            csv_writer.writerow(article)
    except Exception as e:  # this is poor form, change to specific exceptions
        print('Error saving article to file: {}'.format(str(e)))
