import requests
import xlsxwriter
import csv

from utils import file_utils

# need to import


def getArticlesForMultipleStocks(STOCKS, date):

    listArticles=[]

    for stock in STOCKS:
 
        articles = getArticlesForStock(stock, date)

        listArticles.extend(articles)

    return listArticles


def getArticlesForStock(stockSymbol, date):

    url_pattern = ('https://newsapi.org/v2/everything?'
        'q={0}+stock&'
        'from={1}&'
        'sortBy=popularity&'
       'apiKey=ec07e0116ce8450c8b677e877b2e8761')

    url= url_pattern.format(stockSymbol, date)
    response = requests.get(url).json()
    

    print(response)


    listArticles= []

    for article in response["articles"]:
        newTuple= file_utils.createArticle(stockSymbol, article.get('title'), article.get('url'), article.get('content'), article.get('description'), "NewsAPI", article.get('publishedAt')[:10])

        listArticles.append(newTuple)

      
    return listArticles


def processArticlesTuple(listArticles):

  
    results = []

    # Format our article data before writing to file 

    for row in listArticles:
        tabloid = {}
        tabloid['Stock Symbol']= row[0]   
        tabloid['name']= row[1]    
        tabloid['url']= row[2]   
        tabloid['content']= row[3]    
        tabloid['description']= row[4]    
        tabloid['apiSource']= row[5]    
        tabloid['date']= row[6]    
        results.append(tabloid)

    # write to file 

    filename = 'stockArticles2.csv'
    with open(filename, 'a') as f:
        w = csv.DictWriter(f,['Stock Symbol', 'name','url','content', 'description', 'apiSource', 'date'])
        w.writeheader()
        for article in results:
            w.writerow(article) 
       

