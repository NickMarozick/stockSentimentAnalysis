# Sentiment Analysis on News to Predict Stock Performace

# How to run:

1) Clone the project from git
2) Navigate to 'outer_folder' directory
3) ```docker-compose up```
4) In a new terminal enter into the docker shell, ```docker exec -it <container_name> sh```
5) Get into the Django Shell: ```python manage.py shell```
6) Start up the celery beat scheduler: ```celery -A mysite worker --beat -S django -l info```


# Tasks

## Finished

- news scraper (get_stock_articles.py)
- content scraper (get_content_from_articles.py)
- django models created
- stock historical data theough Yahoo Finance API (get_historical_stock_data.py)
- initial views and gainer graphs
- dockerfile and docker-compose

## ToDo

- checkbox to select stocks to study
- auto-add of stocks to study (from gainers/ losers)
- host site
- sentiment analysis (sklearn_sa.py)
- ground truth for articles summary (positive or negative, binary)
- method for comparing senitment analysis results with ground truth
- alert mechanisms for gaining stocks (auto-email)

