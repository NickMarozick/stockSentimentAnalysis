import collections
import csv

FIELDS = ['name', 'url', 'content', 'description', 'scraper']

Article = collections.namedtuple('Article', FIELDS)

def createArticle(name, blah):
    return Article(name, blah)


def saveArticleDetailsToFile(article):
    filename = 'stockNewsArticles.csv'
    try:
        with open(filename, 'a') as f:      # open file in append mode
            csv_writer = csv.DictWriter(f, FIELDS)
            csv_writer.writeheader()
            csv_writer.writerow(article)
    except Exception as e:  # this is poor form, change to specific exceptions
        print('Error saving article to file: {}'.format(str(e)))
