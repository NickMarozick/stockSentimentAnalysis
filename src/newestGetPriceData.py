import sys
from utils import file_utils
from utils import sqlite_utils
from stock_historical_data import getStockData

connnection_pricing_database = sqlite_utils.createConnection(r"/var/stockSA/stockPricing.db")
if connnection_pricing_database is None:
    print("Failed to open database connection")
    sys.exit(1)

getStockData.userSearchAndStoreStockPricingLoop(connnection_pricing_database)
