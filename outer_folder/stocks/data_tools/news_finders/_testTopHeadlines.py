import requests



url_pattern = ('https://newsapi.org/v2/everything?'
    'q=stocks&buy&top&'
    #'sources=bloomberg&business-insider&fortune&'
    'apiKey=ec07e0116ce8450c8b677e877b2e8761')
#url= url_pattern.format()
response = requests.get(url_pattern).json()

#Investor's Business Daily
#Bloomberg
#Seeking Alpha


#bloomberg
#business-insider
#fortune

for article in response["articles"]:
    title = article.get('title')
    print(title)
    print('\n')
