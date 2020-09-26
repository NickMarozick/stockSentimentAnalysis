import sys
from utils import file_utils
from utils import sqlite_utils
from datetime import datetime, timedelta


#STOCKS = ["AAPL", "ABBV", "TXN"]


#date= datetime.today() - timedelta(days=28)

#reformatedDate= str(date.month) + "-" + str(date.day) + "-" + str(date.year)



conn= sqlite_utils._createConnection(r"/var/stockSA/stockPricing.db")

if conn is None:
    print("Failed to open database connection")
    sys.exit(1)

sqlite_utils._createStockPricingTable(conn)

