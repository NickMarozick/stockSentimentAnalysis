import requests
import xlsxwriter
import csv

url = ('https://newsapi.org/v2/everything?'
       'q=NFLX&'
       'from=2019-12-10&'
       'sortBy=popularity&'
       #'apiKey=____')


response= requests.get(url).json()

article = response["articles"]


results=[]


for row in article:
    tabloid = {}
    tabloid['name']= row["title"]
    tabloid['url']= row["url"]
    tabloid['content']= row["content"]
    results.append(tabloid)


#print(results)


filename = 'netflixArticles.csv'
with open(filename, 'w') as f:
    w = csv.DictWriter(f,['name','url','content'])
    w.writeheader()
    for article in results:
        w.writerow(article)
