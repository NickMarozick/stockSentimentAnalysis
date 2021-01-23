import sys
from utils import file_utils
from utils import sqlite_utils
from datetime import datetime, timedelta

# connecting to the database

conn= sqlite_utils.createConnection(r"/var/stockSA/stockPricing.db")

if conn is None:
    print("Failed to open database connection")
    sys.exit(1)

data = sqlite_utils._findAllStockPricingForStockSymbol(conn, ('AAPL'))

print(data)
