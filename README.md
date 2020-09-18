# Sentiment Analysis on News to Predict Stock Performace

# How to run:

Make sure you are using Python3.

In a virtualenv, run: `pip install -f requirements.txt`. This will install
all dependencies.

TBD


# Tasks

## Finished

- news scraper (newsApi.py)
- content scraper (content_scraper.py)
- sqlite utils functions (create db, create table, insert articles, find
  articles by symbol, find articles after date)

## ToDo

- sentiment analysis (sklearn_sa.py)
- ground truth for articles summary (positive or negative, binary)
- method for comparing senitment analysis results with ground truth
- stock data scraper (Yahoo Finance API?)
- database (and helper functions) for stock data
- Python/Jupyter notebook for analysis and visualizations
