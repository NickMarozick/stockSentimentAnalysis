from sentiment_analysis_utils import sklearn_sa

#import xml.etree.ElementTree as ET
#t = ET.parse('/Users/bcopos/Downloads/sorted_data/software/negative.review')
#print(t)
#print(root)


from lxml import etree
from lxml import html

tree = html.parse('/Users/bcopos/Downloads/sorted_data/kitchen_&_housewares/negative.review')
#print(dir(tree))
#print(tree.xmlschema())

from bs4 import BeautifulSoup
f = open('/Users/bcopos/Downloads/sorted_data/kitchen_&_housewares/negative.review', 'rb')
data = f.read()
f.close()
soup = BeautifulSoup(data)
reviews = soup.find_all('review_text')
for review in reviews:
    print(review.text.strip())


#a = sklearn_sa.TransformData()
#b = sklearn_sa.Train()
#c = sklearn_sa.Fit()
